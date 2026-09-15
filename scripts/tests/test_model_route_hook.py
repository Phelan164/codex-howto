from __future__ import annotations

import copy
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model_route_hook import load_policy, route

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "examples/hooks/model-routing/routing.yaml"
SCRIPT = ROOT / "scripts/model_route_hook.py"


class ModelRouteTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.state = self.directory / "routing.sqlite3"
        self.cfg = load_policy(CONFIG)
        self.available = {v["model"]: [v["reasoning_effort"]] for v in self.cfg["tiers"].values()}

    def event(self, tier="easy", role="worker", task="one", call="call-1"):
        return {"hook_event_name": "PreToolUse", "tool_name": "spawn_agent", "session_id": "session-1",
                "tool_use_id": call, "tool_input": {"message": "MODEL_ROUTE " + json.dumps(
                    {"task": task, "tier": tier, "role": role}) + "\nInspect the test result.", "agent_type": "default"}}

    def run_hook(self, event):
        return route(event, self.cfg, self.available, self.state)

    def test_exact_requested_defaults(self):
        self.assertEqual(self.cfg, {"enabled": True, "scope": "subagents", "preserve_explicit_model": True,
            "tiers": {"easy": {"model": "gpt-5.6-luna", "reasoning_effort": "low"},
                      "medium": {"model": "gpt-5.6-sol", "reasoning_effort": "high"},
                      "difficult": {"model": "gpt-6-astra", "reasoning_effort": "high"}},
            "policy": {"uncertain_tier": "difficult", "reviewer_minimum_tier": "medium",
                       "max_escalations_per_task": 1, "unavailable_model": "inherit", "log_decisions": True}})

    def test_each_tier_preserves_other_arguments(self):
        for tier, spec in self.cfg["tiers"].items():
            with self.subTest(tier=tier):
                event = self.event(tier=tier, call=tier, task=tier)
                original = copy.deepcopy(event)
                out = self.run_hook(event)["hookSpecificOutput"]
                expected = dict(event["tool_input"], model=spec["model"], reasoning_effort=spec["reasoning_effort"])
                self.assertEqual(out["updatedInput"], expected)
                self.assertEqual(event, original)
                self.assertEqual(out["permissionDecision"], "allow")

    def test_prompt_policy_does_not_change_model(self):
        result = self.run_hook({"hook_event_name": "UserPromptSubmit"})
        out = result["hookSpecificOutput"]
        self.assertEqual(set(out), {"hookEventName", "additionalContext"})
        self.assertIn("minimum tier of medium", out["additionalContext"])
        self.assertFalse(self.state.exists())

    def test_unmarked_task_uses_difficult(self):
        event = self.event()
        event["tool_input"]["message"] = "Investigate this"
        self.assertEqual(self.run_hook(event)["hookSpecificOutput"]["updatedInput"]["model"], "gpt-6-astra")

    def test_reviewer_floor_from_marker_or_agent_type(self):
        for marker, agent in [("reviewer", "default"), ("worker", "security-reviewer")]:
            event = self.event(role=marker, call=agent)
            event["tool_input"]["agent_type"] = agent
            self.assertEqual(self.run_hook(event)["hookSpecificOutput"]["updatedInput"]["model"], "gpt-5.6-sol")

    def test_preserves_explicit_model_and_effort(self):
        for field, value in [("model", "user-choice"), ("reasoning_effort", "high")]:
            event = self.event(call=field)
            event["tool_input"][field] = value
            self.assertEqual(self.run_hook(event), {})

    def test_explicit_override_opt_out(self):
        self.cfg["preserve_explicit_model"] = False
        event = self.event()
        event["tool_input"]["model"] = "old-choice"
        self.assertEqual(self.run_hook(event)["hookSpecificOutput"]["updatedInput"]["model"], "gpt-5.6-luna")

    def test_unavailable_model_or_effort_inherits(self):
        for inventory in [{}, {"gpt-5.6-luna": ["high"]}]:
            self.available = inventory
            self.assertEqual(self.run_hook(self.event(call=str(inventory))), {})

    def test_full_fork_or_other_adapter_untouched(self):
        for fields in [{"fork_context": True}, {"fork_turns": "all"}, {"items": [{"type": "text"}]}]:
            event = self.event(call=str(fields))
            event["tool_input"].update(fields)
            self.assertEqual(self.run_hook(event), {})

    def test_other_events_and_tools_untouched(self):
        for change in [{"hook_event_name": "Stop"}, {"tool_name": "Bash"}, {"tool_name": "collaboration.spawn_agent"}]:
            event = self.event()
            event.update(change)
            self.assertEqual(self.run_hook(event), {})
        self.assertFalse(self.state.exists())

    def test_disabled_does_nothing(self):
        self.cfg["enabled"] = False
        self.assertEqual(self.run_hook(self.event()), {})
        self.assertEqual(self.run_hook({"hook_event_name": "UserPromptSubmit"}), {})
        self.assertFalse(self.state.exists())

    def test_one_escalation_then_deny_across_turns(self):
        self.run_hook(self.event())
        second = self.event("medium", call="2")
        second["turn_id"] = "next-turn"
        self.assertEqual(self.run_hook(second)["hookSpecificOutput"]["permissionDecision"], "allow")
        self.assertEqual(self.run_hook(self.event("difficult", call="3"))["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_same_tier_retries_do_not_count_as_escalations(self):
        for number in range(3):
            self.run_hook(self.event(call=str(number)))
        self.assertEqual(self.run_hook(self.event("difficult", call="upgrade"))["hookSpecificOutput"]["permissionDecision"], "allow")

    def test_separate_tasks_and_sessions_have_separate_limits(self):
        self.cfg["policy"]["max_escalations_per_task"] = 0
        self.run_hook(self.event())
        self.assertEqual(self.run_hook(self.event("difficult", call="2", task="two"))["hookSpecificOutput"]["permissionDecision"], "allow")
        event = self.event("difficult")
        event["session_id"] = "session-2"
        self.assertEqual(self.run_hook(event)["hookSpecificOutput"]["permissionDecision"], "allow")

    def test_concurrent_identical_calls_are_idempotent(self):
        event = self.event()
        with ThreadPoolExecutor(max_workers=4) as pool:
            outputs = list(pool.map(self.run_hook, [event] * 8))
        self.assertTrue(all(out == outputs[0] for out in outputs))
        with closing(sqlite3.connect(self.state)) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM decisions").fetchone()[0], 1)

    def test_conflicting_call_replay_rejected(self):
        self.run_hook(self.event())
        with self.assertRaises(ValueError):
            self.run_hook(self.event("medium"))

    def test_concurrent_escalations_share_one_counter(self):
        self.run_hook(self.event())
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(self.run_hook, [self.event("medium", call="2"), self.event("medium", call="3")]))
        self.assertTrue(all(out["hookSpecificOutput"]["permissionDecision"] == "allow" for out in results))
        self.assertEqual(self.run_hook(self.event("difficult", call="4"))["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_agent_alias_routes(self):
        event = self.event()
        event["tool_name"] = "Agent"
        self.assertEqual(self.run_hook(event)["hookSpecificOutput"]["updatedInput"]["model"], "gpt-5.6-luna")

    def test_state_symlink_rejected(self):
        target = self.directory / "other"
        target.touch()
        self.state.symlink_to(target)
        with self.assertRaises(ValueError):
            self.run_hook(self.event())

    def test_hook_template_has_only_expected_handlers(self):
        hooks = json.loads((CONFIG.parent / "hooks.json").read_text())["hooks"]
        self.assertEqual(set(hooks), {"UserPromptSubmit", "PreToolUse"})
        self.assertEqual(hooks["PreToolUse"][0]["matcher"], "^(spawn_agent|Agent)$")
        for groups in hooks.values():
            self.assertEqual(groups[0]["hooks"][0]["timeout"], 10)

    def test_logs_exclude_content_and_do_not_invent_actual_usage(self):
        event = self.event()
        event["tool_input"]["message"] += "\nsecret-marker-private"
        self.run_hook(event)
        with closing(sqlite3.connect(self.state)) as db:
            dump = "\n".join(db.iterdump())
            self.assertNotIn("secret-marker-private", dump)
            self.assertNotIn("Inspect the test result", dump)
            self.assertEqual(db.execute("SELECT actual_model, tokens FROM decisions").fetchone(), (None, None))

    def test_disable_logs_keeps_only_required_counter_state(self):
        self.cfg["policy"]["log_decisions"] = False
        self.run_hook(self.event())
        with closing(sqlite3.connect(self.state)) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM decisions").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT count(*) FROM tasks").fetchone()[0], 1)

    def test_bad_metadata_denies(self):
        for text in ["{", "[]", '{"tier":"easy"}', '{"task":"../x","tier":"easy","role":"worker"}']:
            event = self.event()
            event["tool_input"]["message"] = "MODEL_ROUTE " + text
            self.assertEqual(self.run_hook(event)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_missing_identity_rejected(self):
        event = self.event()
        del event["session_id"]
        with self.assertRaises(ValueError):
            self.run_hook(event)

    def test_policy_rejects_typos_types_duplicates_and_unsafe_yaml(self):
        source = CONFIG.read_text()
        for text in [source.replace("scope: subagents", "scope: main"),
                     source.replace("enabled: true", 'enabled: "true"'),
                     source.replace("max_escalations_per_task: 1", "max_escalations_per_task: -1"),
                     source.replace("enabled: true", "enabled: true\n  enabled: false"),
                     "!!python/object/apply:os.system ['false']"]:
            path = self.directory / "bad.yaml"
            path.write_text(text)
            with self.assertRaises((ValueError, __import__("yaml").YAMLError)):
                load_policy(path)

    def test_cli_valid_output_and_safe_failure(self):
        inventory = self.directory / "models.json"
        inventory.write_text(json.dumps(self.available))
        args = [sys.executable, str(SCRIPT), "--config", str(CONFIG), "--available-models", str(inventory), "--state", str(self.state)]
        good = subprocess.run(args, input=json.dumps(self.event()), text=True, capture_output=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)["hookSpecificOutput"]["permissionDecision"], "allow")
        bad = subprocess.run(args, input="secret-invalid-json", text=True, capture_output=True)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(bad.stdout, "")
        self.assertNotIn("secret-invalid-json", bad.stderr)

    def test_disabled_cli_needs_no_inventory_or_state(self):
        config = self.directory / "disabled.yaml"
        config.write_text(CONFIG.read_text().replace("enabled: true", "enabled: false"))
        result = subprocess.run([sys.executable, str(SCRIPT), "--config", str(config),
            "--available-models", str(self.directory / "absent.json"), "--state", str(self.state)],
            input="{}", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertFalse(self.state.exists())


if __name__ == "__main__":
    unittest.main()
