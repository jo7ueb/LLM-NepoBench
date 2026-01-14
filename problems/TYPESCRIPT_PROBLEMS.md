# TypeScript ベンチマーク問題一覧

## 概要

TypeScriptのベンチマーク問題は**59問**で構成されています。基本的な文法・型システムの理解から、TypeScript固有の高度な型システム、フレームワークパターンまで幅広くカバーしています。

## 問題カテゴリ総括

| カテゴリ | 問題数 | 説明 |
|----------|--------|------|
| 基本問題 | 22 | 型安全、非同期、データ処理、OOP、アルゴリズム |
| Agent Level 1-4 | 22 | 設計判断が必要な実践問題 |
| **TypeScript固有** | **15** | **高度な型システム、フレームワーク、バグ修正** |
| **合計** | **59** | |

---

## TypeScript固有の強み（新規追加）

### 高度な型システム（5問）

TypeScriptが他の言語と比較して優れている型システムの活用能力を評価。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_conditional_types` | Conditional Types | Flatten, NonNullable, ReturnType | 3 |
| `ts_mapped_types` | Mapped Types | Readonly, Partial, Required, Mutable | 4 |
| `ts_template_literal` | Template Literal Types | EventName, PathParams | 4 |
| `ts_infer_keyword` | infer キーワード | FirstArg, PromiseValue, ArrayItem | 4 |
| `ts_discriminated_union` | Discriminated Union | Action型、reducer、型安全dispatch | 4 |

### デコレータ（1問）

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_decorators` | デコレータ実装 | @log, @memoize | 2 |

### React パターン（3問）

実際のReactなしでReact風のAPIを実装。フレームワーク理解度を評価。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_react_hooks` | React Hooks | useState, useEffect, useMemo | 3 |
| `ts_react_context` | React Context | createContext, Provider, useContext | 3 |
| `ts_react_reducer` | useReducer | reducer、型安全なdispatch | 3 |

### Express/バックエンド パターン（3問）

サーバーサイドTypeScriptの実践パターン。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_express_middleware` | Express風App | ミドルウェア、ルーティング | 4 |
| `ts_validation_schema` | Zod風スキーマ | z.string(), z.object(), parse() | 5 |
| `ts_orm_query` | ORM風クエリ | Repository, where, find | 4 |

### バグ修正問題（3問）

TypeScript特有の落とし穴を発見・修正する能力を評価。

| ID | 問題名 | バグ内容 | テスト数 |
|----|--------|----------|----------|
| `ts_this_binding_bug` | this バインディング | コールバックでthisが失われる | 3 |
| `ts_equality_bug` | 等価性チェック | オブジェクトの深い比較 | 5 |
| `ts_async_iteration_bug` | 非同期イテレーション | for...of → for await...of | 2 |

---

## 基本問題一覧（22問）

### 型安全（Type Safety）

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `ts_typesafety` | 型安全リファクタ | any を型定義に置き換え | 4 |
| `ts_type_guard` | 型ガード関数 | isString, isNumber, isUser | 8 |
| `ts_generic_function` | ジェネリック関数 | first, last, unique, groupBy | 6 |

### 非同期処理（Async）

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `ts_async_wait` | forEach await バグ修正 | 全件保存待機 | 2 |
| `ts_promise_retry` | リトライ機能 | maxAttempts まで再試行 | 3 |

### データ処理（Data Processing）

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `ts_array_utils` | 配列ユーティリティ | chunk, flatten, zip | 5 |
| `ts_object_utils` | オブジェクトユーティリティ | pick, omit, merge | 4 |
| `ts_string_utils` | 文字列ユーティリティ | capitalize, camelCase変換 | 6 |
| `ts_date_utils` | 日付ユーティリティ | formatDate, addDays | 5 |
| `ts_deep_clone` | 深いコピー | ネストオブジェクト対応 | 3 |
| `ts_debounce_throttle` | debounce/throttle | 実行制御 | 2 |

### OOP / クラス設計

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `ts_event_emitter` | イベントエミッター | on, off, emit | 2 |
| `ts_result_type` | Result型 | Rust風のOk/Err | 4 |

### アルゴリズム / データ構造

| ID | 問題名 | 内容 | テスト数 |
|----|--------|------|----------|
| `ts_observable` | Observable | map, filter 演算子 | 3 |
| `ts_linked_list` | 連結リスト | append, prepend, remove | 4 |
| `ts_binary_search` | 二分探索 | カスタム比較対応 | 4 |
| `ts_tree_traversal` | 木構造走査 | in/pre/post order, BFS | 4 |

---

## エージェント能力評価問題（22問）

### Level 1 (★☆☆☆) - 入門（6問）

基本的な設計判断が必要。要件から適切なAPIを設計する能力を評価。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_agent_L1_storage` | Key-Valueストレージ | TTL設計、API設計 | 5 |
| `ts_agent_L1_validator` | バリデーター | チェーン設計、エラー管理 | 4 |
| `ts_agent_L1_queue` | FIFO キュー | データ構造設計 | 4 |
| `ts_agent_L1_stack` | LIFO スタック | データ構造設計 | 3 |
| `ts_agent_L1_counter` | カウンター | 状態管理 | 4 |
| `ts_agent_L1_timer` | タイマー | 時間計測、状態管理 | 2 |

### Level 2 (★★☆☆) - 中級（7問）

複数の設計判断が必要。既存パターンの適用と応用を評価。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_agent_L2_state_manager` | 状態管理 | subscribe/selector設計 | 4 |
| `ts_agent_L2_router` | URLルーター | パラメータ抽出、マッチング | 4 |
| `ts_agent_L2_cache` | LRUキャッシュ | 削除戦略、TTL | 5 |
| `ts_agent_L2_task_queue` | タスクキュー | 並行制御 | 4 |
| `ts_agent_L2_pub_sub` | Pub/Sub | イベント配信設計 | 3 |
| `ts_agent_L2_promise_pool` | Promise プール | 並行制限 | 2 |
| `ts_agent_L2_retry_with_backoff` | 指数バックオフ | リトライ戦略 | 3 |

### Level 3 (★★★☆) - 上級（5問）

複雑な設計パターンの実装。TypeScriptの型システムを活用した設計を評価。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_agent_L3_di_container` | DIコンテナ | 依存解決、ライフタイム | 4 |
| `ts_agent_L3_state_machine` | 状態マシン | 遷移管理、コールバック | 4 |
| `ts_agent_L3_circuit_breaker` | サーキットブレーカー | 状態遷移、回復戦略 | 5 |
| `ts_agent_L3_command_pattern` | コマンドパターン | Undo/Redo | 4 |
| `ts_agent_L3_interpreter` | 式インタプリタ | パーサー、評価器 | 5 |

### Level 4 (★★★★) - エキスパート（4問）

実務レベルの複雑な問題。複数のデザインパターンを組み合わせた実装を評価。

| ID | 問題名 | 評価観点 | テスト数 |
|----|--------|----------|----------|
| `ts_agent_L4_workflow_engine` | ワークフローエンジン | 依存関係、並列実行 | 4 |
| `ts_agent_L4_saga_pattern` | Saga パターン | 補償処理、ロールバック | 3 |
| `ts_agent_L4_api_gateway` | API ゲートウェイ | ルーティング、ミドルウェア | 5 |
| `ts_agent_L4_event_bus` | イベントバス | ワイルドカード、エラー処理 | 3 |

---

## 採点方式

### 部分点評価

各問題は複数のテストケースで構成されており、通過したテスト数に応じて部分点が付与されます。

```
スコア = (通過テスト数 / 全テスト数) × 100
```

### 例

| 問題 | 全テスト | 通過 | スコア |
|------|----------|------|--------|
| ts_typesafety | 4 | 4 | 100点 |
| ts_typesafety | 4 | 3 | 75点 |
| ts_typesafety | 4 | 2 | 50点 |

---

## LLMレベル別期待スコア

| LLMレベル | 基本問題 | TypeScript固有 | L1 | L2 | L3 | L4 |
|-----------|----------|----------------|-----|-----|-----|-----|
| 初級 | 60-70% | 40% | 50% | 30% | 10% | 0% |
| 中級 | 80-90% | 60% | 70% | 50% | 30% | 10% |
| 上級 | 95%+ | 80% | 90% | 70% | 50% | 30% |
| エキスパート | 100% | 95%+ | 100% | 90% | 70% | 50% |

---

## TypeScript vs Python 比較

| 項目 | Python | TypeScript |
|------|--------|------------|
| 総問題数 | 55 | 59 |
| 基本問題 | 16 | 22 |
| エージェント問題 | 39 | 22 |
| 言語固有問題 | - | 15（高度な型システム等）|
| フレームワーク問題 | FastAPI | React, Express風 |

TypeScriptは型システムの深い理解が重要なため、Conditional Types、Mapped Types、Template Literal Typesなど**TypeScript固有の問題を15問**追加しています。

---

## 技術要件

### 使用フレームワーク
- **テストフレームワーク**: Vitest
- **TypeScript**: 5.x
- **実行環境**: Node.js 20

### 出力形式
```typescript
// すべてのエクスポートを export で明示
export type User = { name: string; age: number };
export function processUser(user: User) { ... }
```

---

## 更新履歴

| 日付 | 変更内容 |
|------|----------|
| 2026-01-14 | TypeScript固有問題15問追加（高度な型、React/Express、バグ修正）|
| 2026-01-14 | 初版作成（44問）|
