"use client";

import { useMemo, useState } from "react";

type Variant = {
  id: "control" | "full" | "lean";
  label: string;
  shortLabel: string;
  tokens: number;
  seconds: number;
  retries: number;
  accepted: boolean;
};

type Task = {
  id: "backend" | "game";
  eyebrow: string;
  title: string;
  description: string;
  finding: string;
  detail: string;
  source: string;
  sourceLabel: string;
  variants: Variant[];
};

const tasks: Task[] = [
  {
    id: "backend",
    eyebrow: "Small, bounded fix",
    title: "Inventory boundary defect",
    description:
      "One strongly specified Python defect, a six-line final diff, and a complete test suite.",
    finding: "No repository skill used the fewest tokens.",
    detail:
      "The lean loop added 2.9% token overhead versus the control. All three variants found the same defect and passed every required check.",
    source:
      "https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/gpt-5.6-sol-backend-boundary-2026-07-31.md",
    sourceLabel: "Read the backend measurement",
    variants: [
      {
        id: "control",
        label: "No repository skill",
        shortLabel: "No skill",
        tokens: 390144,
        seconds: 114,
        retries: 0,
        accepted: true,
      },
      {
        id: "full",
        label: "Engineering loop v0.2.0",
        shortLabel: "Full v0.2",
        tokens: 418029,
        seconds: 125,
        retries: 1,
        accepted: true,
      },
      {
        id: "lean",
        label: "Lean engineering loop v0.4.0",
        shortLabel: "Lean v0.4",
        tokens: 401602,
        seconds: 125,
        retries: 2,
        accepted: true,
      },
    ],
  },
  {
    id: "game",
    eyebrow: "Medium implementation",
    title: "Dependency-free 2048",
    description:
      "Four browser-game files, ten engine tests, syntax checks, and a post-run evaluator.",
    finding: "The lean loop used 54.0% fewer tokens than the control.",
    detail:
      "It also used 31.2% fewer tokens than v0.2.0 and finished 29.4% faster than the control. Every variant still passed.",
    source:
      "https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/gpt-5.6-sol-2048-game-2026-07-31.md",
    sourceLabel: "Read the 2048 measurement",
    variants: [
      {
        id: "control",
        label: "No repository skill",
        shortLabel: "No skill",
        tokens: 828446,
        seconds: 350,
        retries: 1,
        accepted: true,
      },
      {
        id: "full",
        label: "Engineering loop v0.2.0",
        shortLabel: "Full v0.2",
        tokens: 553179,
        seconds: 257,
        retries: 1,
        accepted: true,
      },
      {
        id: "lean",
        label: "Lean engineering loop v0.4.0",
        shortLabel: "Lean v0.4",
        tokens: 380767,
        seconds: 247,
        retries: 0,
        accepted: true,
      },
    ],
  },
];

const formatTokens = (tokens: number) =>
  new Intl.NumberFormat("en-US").format(tokens);

export default function Home() {
  const [taskId, setTaskId] = useState<Task["id"]>("game");
  const task = tasks.find((item) => item.id === taskId) ?? tasks[1];
  const maxTokens = Math.max(...task.variants.map((variant) => variant.tokens));
  const bestId = useMemo(
    () =>
      task.variants.reduce((best, candidate) =>
        candidate.tokens < best.tokens ? candidate : best,
      ).id,
    [task],
  );

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Codex How To benchmark home">
          <span className="brand-mark" aria-hidden="true">
            C
          </span>
          <span>Codex How To</span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#results">Results</a>
          <a href="#method">Method</a>
          <a
            className="nav-cta"
            href="https://github.com/Phelan164/codex-howto"
          >
            GitHub ↗
          </a>
        </nav>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="kicker">Six controlled GPT-5.6-sol runs</p>
          <h1>
            Do Codex skills
            <br />
            save tokens? <em>It depends.</em>
          </h1>
          <p className="hero-lede">
            The same engineering-loop skill lost on a small fix and won on a
            medium build. Explore the result, inspect the evidence, then run
            your own replication.
          </p>
          <div className="hero-actions">
            <a className="button button-primary" href="#results">
              Explore the benchmark
            </a>
            <a
              className="button button-secondary"
              href="https://github.com/Phelan164/codex-howto/issues/23"
            >
              Replicate it ↗
            </a>
          </div>
        </div>

        <aside className="hero-proof" aria-label="Benchmark summary">
          <div className="proof-grid">
            <div>
              <strong>6</strong>
              <span>controlled runs</span>
            </div>
            <div>
              <strong>6/6</strong>
              <span>accepted</span>
            </div>
            <div>
              <strong>2</strong>
              <span>task sizes</span>
            </div>
            <div>
              <strong>0</strong>
              <span>human corrections</span>
            </div>
          </div>
          <p>
            Quality gates came first. Token use was compared only after every
            variant passed.
          </p>
        </aside>
      </section>

      <section className="results-section" id="results">
        <div className="section-heading">
          <div>
            <p className="kicker">Task-size boundary</p>
            <h2>One skill. Opposite outcomes.</h2>
          </div>
          <div className="task-switcher" aria-label="Choose benchmark task">
            {tasks.map((item) => (
              <button
                className={taskId === item.id ? "active" : ""}
                key={item.id}
                onClick={() => setTaskId(item.id)}
                type="button"
                aria-pressed={taskId === item.id}
              >
                <span>{item.eyebrow}</span>
                {item.id === "backend" ? "Backend fix" : "2048 build"}
              </button>
            ))}
          </div>
        </div>

        <div className="results-grid">
          <article className="chart-card">
            <div className="chart-header">
              <div>
                <p>{task.eyebrow}</p>
                <h3>{task.title}</h3>
              </div>
              <span className="accepted-pill">All passed</span>
            </div>
            <p className="task-description">{task.description}</p>

            <div className="bar-chart" aria-label="Reported token comparison">
              {task.variants.map((variant) => {
                const width = Math.max(16, (variant.tokens / maxTokens) * 100);
                const isBest = variant.id === bestId;

                return (
                  <div className="bar-row" key={variant.id}>
                    <div className="bar-label">
                      <span>{variant.shortLabel}</span>
                      {isBest && <small>fewest tokens</small>}
                    </div>
                    <div className="bar-track">
                      <div
                        className={`bar-fill bar-${variant.id} ${
                          isBest ? "best" : ""
                        }`}
                        style={{ width: `${width}%` }}
                      />
                    </div>
                    <strong>{formatTokens(variant.tokens)}</strong>
                  </div>
                );
              })}
            </div>

            <div className="metric-table" role="table" aria-label="Run details">
              <div className="metric-row metric-head" role="row">
                <span role="columnheader">Variant</span>
                <span role="columnheader">Time</span>
                <span role="columnheader">Retries</span>
                <span role="columnheader">Accepted</span>
              </div>
              {task.variants.map((variant) => (
                <div className="metric-row" role="row" key={variant.id}>
                  <span role="cell">{variant.label}</span>
                  <span role="cell">{variant.seconds}s</span>
                  <span role="cell">{variant.retries}</span>
                  <span role="cell" className="pass">
                    {variant.accepted ? "Yes" : "No"}
                  </span>
                </div>
              ))}
            </div>
          </article>

          <aside className="finding-card">
            <span className="finding-number">
              {task.id === "backend" ? "+2.9%" : "−54.0%"}
            </span>
            <p className="finding-label">
              {task.id === "backend"
                ? "lean skill vs control"
                : "lean skill vs control"}
            </p>
            <h3>{task.finding}</h3>
            <p>{task.detail}</p>
            <a href={task.source}>{task.sourceLabel} ↗</a>
          </aside>
        </div>
      </section>

      <section className="method-section" id="method">
        <div className="section-heading compact">
          <div>
            <p className="kicker">What was held constant</p>
            <h2>Evidence before conclusions.</h2>
          </div>
          <p>
            Same model, reasoning effort, starting commit, task contract,
            sandbox, and acceptance criteria. Only repository-skill routing
            changed.
          </p>
        </div>

        <div className="method-grid">
          <article>
            <span>01</span>
            <h3>Quality first</h3>
            <p>
              Acceptance, required checks, and evidence completeness were
              primary. A cheaper failed run would not win.
            </p>
          </article>
          <article>
            <span>02</span>
            <h3>Three variants</h3>
            <p>
              No repository skill, the original v0.2.0 loop, and the lean
              v0.4.0 loop started from equivalent fresh copies.
            </p>
          </article>
          <article>
            <span>03</span>
            <h3>Reported usage</h3>
            <p>
              Token totals are Codex CLI input plus output tokens. Cached input
              is already included and was not counted twice.
            </p>
          </article>
        </div>
      </section>

      <section className="limits-section">
        <div>
          <p className="kicker">Read this before sharing</p>
          <h2>This is a boundary to test, not a universal claim.</h2>
        </div>
        <ul>
          <li>Two seeded tasks and six total runs are not a population.</li>
          <li>Global personal skills remained visible to every run.</li>
          <li>Run order was fixed, not randomized.</li>
          <li>Live browser behavior could not be verified in the sandbox.</li>
          <li>Independent replications may—and should—disagree.</li>
        </ul>
      </section>

      <section className="cta-section">
        <div>
          <p className="kicker">Make the evidence better</p>
          <h2>Run the protocol on your task.</h2>
          <p>
            Fork the fixture, hold the environment constant, report every
            result, and publish negative findings too.
          </p>
        </div>
        <div className="cta-actions">
          <a
            className="button button-light"
            href="https://github.com/Phelan164/codex-howto/issues/23"
          >
            Join the replication
          </a>
          <a
            className="button button-ghost"
            href="https://github.com/Phelan164/codex-howto/fork"
          >
            Fork an edition ↗
          </a>
        </div>
      </section>

      <footer>
        <p>
          Built from the open measurements in{" "}
          <a href="https://github.com/Phelan164/codex-howto">
            Phelan164/codex-howto
          </a>
          .
        </p>
        <p>Measured 2026-07-31 · GPT-5.6-sol · Codex CLI 0.143.0</p>
      </footer>
    </main>
  );
}
