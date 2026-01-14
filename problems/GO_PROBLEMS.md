# Go ベンチマーク問題一覧

## 概要

Goのベンチマーク問題は**31問**で構成されています。Goらしい並行処理、エラーハンドリング、interface設計を重点的に評価します。

## 問題カテゴリ総括

| カテゴリ | 問題数 | 説明 |
|----------|--------|------|
| 基本問題（Interface） | 2 | interface、Stringer |
| 基本問題（並行処理） | 3 | goroutine、channel、fan-out/in |
| 基本問題（エラー処理） | 2 | カスタムエラー、wrap/unwrap |
| 基本問題（データ構造） | 2 | Stack、Queue（generics） |
| 基本問題（関数型） | 1 | Map/Filter/Reduce |
| Agent Level 1 | 4 | ワーカープール、タイムアウト、キャッシュ等 |
| Agent Level 2 | 4 | context、リトライ、セマフォ、Pub/Sub |
| Agent Level 3 | 4 | サーキットブレーカー、プール、状態マシン等 |
| Agent Level 4 | 4 | イベントソーシング、Saga、スケジューラ、Raftログ |
| HTTP | 2 | ハンドラ、ミドルウェア |
| I/O | 1 | Reader/Writer |
| sync活用 | 2 | Once、Pool |
| **合計** | **31** | |

---

## Goらしさを評価するポイント

### 1. 並行処理（goroutine/channel）
- Fan-out/Fan-in パターン
- Worker Pool
- セマフォ
- Pub/Sub

### 2. エラー処理
- カスタムエラー型
- `errors.Is` / `errors.As`
- エラーのラップ

### 3. context活用
- キャンセレーション
- タイムアウト

### 4. interface設計
- 暗黙的実装
- io.Reader/Writer
- fmt.Stringer

### 5. sync パッケージ
- WaitGroup
- Mutex / RWMutex
- Once
- Pool

### 6. generics（Go 1.18+）
- 型パラメータ
- constraints

---

## 問題一覧

### 基本問題: Interface

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_polymorphism` | ポリモーフィズム | Speaker interface、Dog/Cat | 1 |
| `go_stringer` | fmt.Stringer | String()メソッド実装 | 2 |

### 基本問題: 並行処理

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_concurrent_map` | 並行マップ | goroutine + WaitGroup | 2 |
| `go_channel_pipeline` | パイプライン | Generator → Double → Sum | 3 |
| `go_fan_out_in` | Fan-out/Fan-in | 複数worker、統合 | 1 |

### 基本問題: エラー処理

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_custom_error` | カスタムエラー | ValidationError、errors.As | 3 |
| `go_error_wrap` | エラーラップ | fmt.Errorf、errors.Is | 3 |

### 基本問題: データ構造（generics）

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_stack` | スタック | Stack[T any]、LIFO | 3 |
| `go_queue` | キュー | Queue[T any]、FIFO | 3 |

### 基本問題: 関数型スタイル

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_map_filter_reduce` | Map/Filter/Reduce | ジェネリクス活用 | 4 |

---

## エージェント能力評価問題

### Level 1 (★☆☆☆) - 基本的な並行処理

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `go_agent_L1_worker` | ワーカープール | goroutine管理、ジョブ処理 | 1 |
| `go_agent_L1_timeout` | タイムアウト処理 | select、time.After | 3 |
| `go_agent_L1_cache` | スレッドセーフキャッシュ | sync.RWMutex | 3 |
| `go_agent_L1_rate_limiter` | レートリミッター | トークンバケット | 1 |

### Level 2 (★★☆☆) - Context、高度なエラー処理

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `go_agent_L2_context_cancel` | Contextキャンセル | context.WithTimeout | 2 |
| `go_agent_L2_retry` | リトライ | 指数バックオフ | 2 |
| `go_agent_L2_semaphore` | セマフォ | 同時実行制限 | 2 |
| `go_agent_L2_pubsub` | Pub/Sub | channel、goroutine | 2 |

### Level 3 (★★★☆) - 設計パターン

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `go_agent_L3_circuit_breaker` | サーキットブレーカー | 状態遷移、障害対応 | 3 |
| `go_agent_L3_pool` | コネクションプール | リソース管理、タイムアウト | 3 |
| `go_agent_L3_state_machine` | 状態マシン | 遷移定義、コールバック | 3 |
| `go_agent_L3_middleware` | ミドルウェア | チェーン、next() | 1 |

### Level 4 (★★★★) - 高度な実装

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `go_agent_L4_event_sourcing` | イベントソーシング | イベント記録、状態復元 | 3 |
| `go_agent_L4_saga` | Sagaパターン | 分散トランザクション、補償 | 2 |
| `go_agent_L4_scheduler` | タスクスケジューラ | 定期/遅延実行、キャンセル | 3 |
| `go_agent_L4_raft_log` | Raftログ | 分散合意、コミット | 4 |

---

## 追加問題

### HTTP/ネットワーク

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_http_handler` | HTTPハンドラ | Health、Echo | 2 |
| `go_http_middleware` | HTTPミドルウェア | Logging、Recovery、Auth | 2 |

### I/O

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_reader_writer` | Reader/Writer | CountingReader、LimitWriter | 2 |

### sync パッケージ活用

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `go_sync_once` | sync.Once | シングルトン | 2 |
| `go_sync_pool` | sync.Pool | バッファプール | 1+bench |

---

## 採点方式

### 部分点評価

各問題は複数のテストケースで構成されており、通過したテスト数に応じて部分点が付与されます。

```
スコア = (通過テスト数 / 全テスト数) × 100
```

---

## 技術要件

### 使用バージョン
- **Go**: 1.22+
- **テストフレームワーク**: 標準 testing パッケージ

### 出力形式
```go
package bench

// 必ず package bench を使用
type Stack[T any] struct { ... }
func (s *Stack[T]) Push(v T) { ... }
```

---

## LLMレベル別期待スコア

| LLMレベル | 基本問題 | L1 | L2 | L3 | L4 |
|-----------|----------|-----|-----|-----|-----|
| 初級 | 50-60% | 40% | 20% | 10% | 0% |
| 中級 | 70-80% | 60% | 40% | 25% | 10% |
| 上級 | 90%+ | 80% | 60% | 40% | 25% |
| エキスパート | 95%+ | 95% | 80% | 60% | 40% |

---

## 言語別比較

| 言語 | 問題数 | 特徴 |
|------|--------|------|
| Python | 55 | 基本文法〜AIエージェント向け |
| TypeScript | 59 | 型システム、React/Express |
| **Go** | **31** | **並行処理、エラー処理、interface** |

Goは他言語より問題数は少ないですが、**goroutine/channel**、**context**、**error handling**といったGo特有の概念を深く評価する問題構成になっています。

---

## 更新履歴

| 日付 | 変更内容 |
|------|----------|
| 2026-01-14 | 初版作成（31問）|
