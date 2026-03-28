## ADDED Requirements

### Requirement: 自动重试机制
系统 SHALL 在爬虫失败时自动重试，默认重试 3 次，重试间隔递增。

#### Scenario: 首次失败后重试
- **WHEN** 爬虫首次执行失败
- **THEN** 系统等待 5 秒后自动重试

#### Scenario: 多次重试后仍失败
- **WHEN** 爬虫重试 3 次后仍然失败
- **THEN** 系统记录最终失败状态并停止重试

#### Scenario: 重试成功
- **WHEN** 爬虫在第 2 次重试时成功
- **THEN** 系统记录成功状态并标注重试次数

### Requirement: 可配置的重试策略
系统 SHALL 允许为不同类型的错误配置不同的重试策略。

#### Scenario: 网络错误重试策略
- **WHEN** 爬虫因网络错误失败
- **THEN** 系统使用指数退避策略重试（5s, 10s, 20s）

#### Scenario: API 限流重试策略
- **WHEN** 爬虫因 API 限流失败
- **THEN** 系统等待更长时间后重试（60s, 120s, 180s）

#### Scenario: 解析错误不重试
- **WHEN** 爬虫因解析错误失败
- **THEN** 系统不进行重试，直接记录失败

### Requirement: 统一的错误处理基类
系统 SHALL 提供 BaseCrawlerWithRetry 基类，封装重试逻辑和错误处理。

#### Scenario: 继承基类的爬虫自动获得重试能力
- **WHEN** 新爬虫继承 BaseCrawlerWithRetry 基类
- **THEN** 该爬虫自动具备重试和错误分类能力

#### Scenario: 自定义重试参数
- **WHEN** 爬虫需要自定义重试次数和间隔
- **THEN** 系统允许通过构造函数参数覆盖默认配置
