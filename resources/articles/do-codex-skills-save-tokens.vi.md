---
title: "Skill Codex có giúp tiết kiệm token không? Kết quả từ sáu lượt chạy có kiểm soát"
published: false
description: "Thí nghiệm ưu tiên chất lượng với GPT-5.6-sol cho thấy cùng một engineering skill tạo overhead ở task nhỏ nhưng tiết kiệm token ở task cỡ vừa."
tags: codex, ai, testing, opensource
---

# Skill Codex có giúp tiết kiệm token không? Kết quả từ sáu lượt chạy có kiểm soát

Câu trả lời trung thực không phải là “có” hoặc “không”. Kết quả **phụ thuộc
vào loại task**.

Tôi thực hiện sáu lượt chạy engineering có kiểm soát với GPT-5.6-sol trên hai
kích thước task. Mọi biến thể đều vượt qua acceptance gate mà không cần con
người sửa code.
Với một backend fix nhỏ và được mô tả chặt chẽ, lượt chạy không dùng repository
skill có tổng reported token thấp nhất. Với một task cỡ vừa xây dựng game 2048
không có dependency, bản `engineering-loop` tinh gọn dùng ít hơn nhóm đối chứng
54,0% reported token.

Sự đảo chiều này mới là kết quả hữu ích. Một workflow skill có context cost và
phải tạo ra đủ giá trị cho task hiện tại để bù lại chi phí đó.

Công khai mối liên hệ: tôi duy trì
[Codex How To](https://github.com/Phelan164/codex-howto), repository mã nguồn
mở chứa skill, fixture, evaluator và dữ liệu đo được dùng trong bài viết này.

Dùng
[benchmark explorer tương tác](https://codex-howto-benchmark.nguyenvantamdk2.chatgpt.site)
để chuyển giữa hai kích thước task, xem tỷ lệ token và truy ngược từng kết quả
về bản ghi đo gốc.

Đây là bản tiếng Việt của
[bài viết tiếng Anh](do-codex-skills-save-tokens.md), được đồng bộ lần cuối
ngày 2026-08-03. Nếu hai bản khác nhau, số liệu và phương pháp trong bản tiếng
Anh là nguồn chuẩn.

## Giả thuyết tôi muốn kiểm tra

Repository xem code do mô hình sinh ra là kết quả trung gian. Skill
`engineering-loop` yêu cầu Codex:

1. xác định phạm vi task;
2. reproduce vấn đề hoặc thiết lập baseline;
3. thực hiện thay đổi nhỏ nhất nhưng vẫn hoàn chỉnh;
4. chạy focused check và các check bắt buộc của repository;
5. review diff tạo ra; và
6. bàn giao bằng chứng đã kiểm chứng cùng residual risk.

Đây là lời khuyên engineering hợp lý. Tuy nhiên, GPT-5.6-sol vốn đã biết nhiều
về quy trình phát triển phần mềm. Nạp một lifecycle skill cho mọi task có thể
lặp lại hành vi mô hình tự làm, tốn thêm context hoặc kích hoạt các check không
cần thiết.

Vì vậy, câu hỏi hẹp hơn “skill có tốt không?” là:

> Khi nào repository skill này cải thiện một engineering task đã hoàn thành đủ
> để bù cho context cost và execution cost của nó?

## Chất lượng được ưu tiên trước số token

Điều kiện chấp nhận chính là đáp ứng acceptance criteria mà không cần con người
sửa code. Token, elapsed time và số lần retry là chỉ số phụ.

Với mỗi task, ba biến thể bắt đầu từ các Git repository mới và tương đương:

- không dùng repository skill;
- `engineering-loop` v0.2.0; và
- `engineering-loop` v0.4.0 bản tinh gọn.

Trong từng nhóm task, model, medium reasoning effort, starting commit, bề mặt
Codex CLI, workspace-write sandbox, task contract, tool và acceptance criteria
được giữ cố định.

Hai biến thể có skill gọi trực tiếp repository skill đã cài. Nhóm đối chứng
không cài hoặc nhắc tên skill đó. Các personal skill ở cấp global vẫn hiển thị
với mọi lượt chạy, vì vậy “không dùng repository skill” **không** có nghĩa là
model không nhận bất kỳ instruction nào. Thực tế, các lượt đối chứng tự động
chọn global skill. Đây là một hạn chế, nhưng cũng gần với môi trường Codex đã
được cấu hình trong thực tế.

Tổng reported token là input token cộng output token do Codex CLI báo cáo.
Cached input đã nằm trong input count và không được cộng lần thứ hai.

## Kết quả 1: fix nhỏ không cần lifecycle skill

Task đầu tiên là một lỗi inventory Python có phạm vi hẹp. Codex phải tìm boundary
zero-quantity chưa được cover, giữ lại regression đang fail trước khi sửa, thực
hiện correction nhỏ nhất, chạy test bắt buộc, review diff và báo cáo residual
input risk.

| Variant | Accepted | Reported token | Elapsed | Retry |
|---|---:|---:|---:|---:|
| Không dùng repository skill | có | 390.144 | 114 giây | 0 |
| Full skill v0.2.0 | có | 418.029 | 125 giây | 1 |
| Lean skill v0.4.0 | có | 401.602 | 125 giây | 2 |

Cả ba biến thể đều:

- tìm ra cùng một defect;
- thêm cùng một guard hai dòng;
- thêm regression test bốn dòng;
- pass focused suite và toàn bộ backend suite;
- xóa thay đổi bytecode sinh tự động;
- review diff cuối gồm hai file, sáu dòng; và
- xác định cùng một risk chưa test với input không phải integer và input boolean.

Nhóm đối chứng dùng ít token và retry nhất. Lean skill dùng nhiều hơn nhóm đối
chứng khoảng 2,9% reported token, dù ít hơn full skill cũ khoảng 3,9%.

Với task này, repository contract tốt cùng hành vi sẵn có của model đã đủ.
Lifecycle skill không tạo khác biệt về chất lượng được chấp nhận.

Đọc đầy đủ
[bản đo backend](https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/gpt-5.6-sol-backend-boundary-2026-07-31.md).

## Kết quả 2: task cỡ vừa có lợi khi dùng lean skill

Task thứ hai xây dựng phiên bản 2048 chạy trên browser mà không có dependency.
Nó yêu cầu bốn product file, engine có hành vi deterministic, điều khiển bằng
keyboard và touch, tính điểm, restart, mười test được cung cấp, syntax check và
post-run evaluator.

| Variant | Accepted | Reported token | Elapsed | Retry |
|---|---:|---:|---:|---:|
| Không dùng repository skill | có | 828.446 | 350 giây | 1 |
| Full skill v0.2.0 | có | 553.179 | 257 giây | 1 |
| Lean skill v0.4.0 | có | 380.767 | 247 giây | 0 |

Một lần nữa, mọi biến thể đều pass:

- toàn bộ mười engine test;
- JavaScript syntax check;
- mọi post-run evaluator check;
- ràng buộc không dependency và không network; và
- yêu cầu cuối về evidence và diff review.

Lean skill dùng:

- **ít hơn nhóm đối chứng không dùng repository skill 54,0% reported token**;
- **ít hơn v0.2.0 31,2% reported token**;
- **ít hơn nhóm đối chứng 29,4% elapsed time**; và
- không có lượt thử lặp lại mà không tạo thêm bằng chứng.

Khác biệt hành vi chính không đơn giản là “chạy ít check hơn”. Browser execution
không khả dụng trong sandbox. Lean run xác nhận giới hạn đó rồi dừng. Các biến
thể còn lại tiếp tục thử thêm những cách launch khác dù boundary đã rõ.

Đọc đầy đủ
[bản đo 2048](https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/gpt-5.6-sol-2048-game-2026-07-31.md).

## Boundary hữu ích hơn việc chọn một bên thắng

Hai nhóm task gợi ý một giả thuyết đáng kiểm tra:

- **Fix nhỏ, specification chặt:** lifecycle skill có thể lặp lại hành vi model
  và repository instruction đã cung cấp.
- **Task có nhiều bề mặt implementation và verification:** lifecycle guidance
  ngắn gọn có thể ngăn việc khám phá lặp lại và giúp model dừng khi không còn
  cách verification khả dụng.

Điều này không có nghĩa chỉ cần nhìn kích thước task để chọn skill. Risk, độ mơ
hồ, chất lượng repository, tool hiện có và chi phí nếu bỏ sót một check cũng
quan trọng. Một authorization bug năm dòng có thể cần quy trình chặt hơn một
static demo một trăm dòng.

Quy tắc thực tế là:

> Dùng workflow nhỏ nhất vẫn bảo vệ acceptance criteria, sau đó đo xem nó có bù
> được context cost cho loại task đó hay không.

## Thí nghiệm này không chứng minh điều gì

Sáu lượt chạy không đủ để đại diện cho một tổng thể. Kết quả chỉ nên được xem
là seed measurement vì:

- chỉ có hai task;
- mọi lượt chạy đều nhìn thấy cùng personal skill catalog global;
- thứ tự chạy được cố định thay vì random;
- evaluator biết từng biến thể sau khi chạy;
- không thể verify hành vi browser thực trong sandbox;
- CLI phát model-cache schema warning trong quá trình chạy; và
- không thu thập được phép đo về chi phí và số dòng context noise.

Game fixture cũng nhấn mạnh deterministic engine behavior hơn visual polish.
Một product task thực tế có thể tạo ra boundary khác.

Vì vậy, replication có kết quả tiêu cực hoặc trung tính có giá trị hơn việc chỉ
xác nhận kết quả hiện tại.

## Cách reproduce

Dùng ba bản sao mới của cùng một task repository:

1. không dùng repository skill;
2. dùng full skill hiện tại hoặc team-default skill; và
3. dùng lean skill chỉ chứa workflow contract thiết yếu.

Giữ cố định:

- model và reasoning effort;
- starting commit và dependency state;
- task prompt và acceptance criteria;
- tool và permission hiện có;
- sandbox và bề mặt Codex; và
- evaluator hoặc rubric.

Đăng ký quality gate trước khi chạy. Ghi lại acceptance, mức đầy đủ của
evidence, required check, retry, human correction, elapsed time và reported
token. Không so sánh efficiency nếu một biến thể fail quality gate.

Đổi thứ tự chạy giữa các replication và công bố mọi kết quả, kể cả khi skill
tạo overhead hoặc không tạo khác biệt.

Repository cung cấp
[measurement protocol](https://github.com/Phelan164/codex-howto/blob/main/resources/engineering-loop-measurement.md),
[CSV schema](https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/engineering-loop-runs.csv),
[2048 fixture](https://github.com/Phelan164/codex-howto/tree/main/labs/2048-game-benchmark)
và
[replication request](https://github.com/Phelan164/codex-howto/issues/23)
đang mở.

## Tôi muốn thấy kết quả này bị bác bỏ ở đâu

Bằng chứng hữu ích tiếp theo không phải thêm một seeded demo từ maintainer, mà
là một task bên ngoài có tính đại diện:

- frontend change cần visual verification;
- infrastructure change có preview và rollback constraint;
- defect mơ hồ cần khám phá repository; hoặc
- security-sensitive change nơi chi phí bỏ sót review finding lớn hơn token cost.

Nếu bạn chạy một task, hãy báo cáo starting condition và quality gate, không
chỉ tổng token. Nếu kết quả của bạn mâu thuẫn với boundary về task size này, dự
án sẽ tốt hơn.

Xem, reproduce hoặc fork toàn bộ package tại
[Phelan164/codex-howto](https://github.com/Phelan164/codex-howto). Chỉ star khi
các measurement và workflow đủ hữu ích để bạn muốn quay lại.
