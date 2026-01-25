# SMEL Grammar Files

这个目录包含三个 SMEL 语法定义文件，用于学术研究和对比分析。

## 语法文件

### 1. SMEL.g4（原始版本）
- **用途**: 原始的 SMEL 语法定义
- **特点**: 使用通用操作 + 类型参数（如 `ADD ATTRIBUTE`, `DELETE ENTITY`）
- **文件扩展名**: `.smel`
- **解析器文件**: `SMELLexer.py`, `SMELParser.py`, `SMELListener.py`

### 2. SMEL_Specific.g4（具体操作版）
- **用途**: 每个操作都有独立的关键字
- **特点**:
  - 每个操作都是独立的关键字（如 `ADD_ATTRIBUTE`, `DELETE_ENTITY`）
  - 关键字数量多，但语义明确
  - 易于阅读和理解
- **文件扩展名**: `.smel`
- **解析器文件**: `SMEL_SpecificLexer.py`, `SMEL_SpecificParser.py`, `SMEL_SpecificListener.py`
- **测试文件目录**: `tests/specific/`

**示例**:
```smel
MIGRATION person_migration:1.0
FROM DOCUMENT TO RELATIONAL
USING person_schema:1

ADD_ATTRIBUTE email TO Customer WITH TYPE String NOT NULL
DELETE_ATTRIBUTE Customer.phone
RENAME_FEATURE old_name TO new_name IN Customer
FLATTEN person.address AS address
```

### 3. SMEL_Pauschalisiert.g4（通用参数化版）
- **用途**: 使用通用操作 + 参数的设计
- **特点**:
  - 使用少量通用关键字（如 `ADD_PS`, `DELETE_PS`）+ 类型参数
  - 关键字数量少，扩展性强
  - 参数化设计，易于添加新功能
- **文件扩展名**: `.smel_ps`
- **解析器文件**: `SMEL_PauschalisiertLexer.py`, `SMEL_PauschalisiertParser.py`, `SMEL_PauschalisiertListener.py`
- **测试文件目录**: `tests/pauschalisiert/`

**示例**:
```smel
MIGRATION person_migration:1.0
FROM DOCUMENT TO RELATIONAL
USING person_schema:1

ADD_PS ATTRIBUTE email TO Customer WITH TYPE String NOT NULL
DELETE_PS ATTRIBUTE Customer.phone
RENAME_PS FEATURE old_name TO new_name IN Customer
FLATTEN_PS person.address AS address
```

## 两种设计的对比

| 特性 | SMEL_Specific.g4 | SMEL_Pauschalisiert.g4 |
|------|------------------|------------------------|
| **操作关键字** | 独立、具体（如 `ADD_ATTRIBUTE`） | 通用 + 参数（如 `ADD_PS ATTRIBUTE`） |
| **关键字数量** | 多（每个操作一个） | 少（通用操作 + 类型参数） |
| **可读性** | 高（一目了然） | 中（需要理解参数） |
| **扩展性** | 低（新操作需要新关键字） | 高（只需添加参数） |
| **语法复杂度** | 低（结构简单） | 中（需要参数系统） |
| **文件扩展名** | `.smel` | `.smel_ps` |

## 生成解析器

### 方法1: 使用批处理脚本（Windows）

我们提供了便捷的批处理脚本来生成所有解析器：

```batch
# 生成原始 SMEL 解析器
generate_parser.bat

# 生成 Specific 版本解析器
generate_parser_specific.bat

# 生成 Pauschalisiert 版本解析器
generate_parser_pauschalisiert.bat
```

### 方法2: 手动生成

从 `grammar/` 目录运行以下命令：

```bash
# 生成 SMEL_Specific.g4 解析器
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor SMEL_Specific.g4

# 生成 SMEL_Pauschalisiert.g4 解析器
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor SMEL_Pauschalisiert.g4

# 生成原始 SMEL.g4 解析器
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor SMEL.g4
```

## 生成的文件

每个语法文件会生成以下 Python 文件：

- `*Lexer.py` - 词法分析器
- `*Parser.py` - 语法分析器
- `*Listener.py` - 监听器（用于遍历解析树）
- `*Visitor.py` - 访问器（用于遍历解析树）
- `*.interp` - ANTLR 内部文件
- `*.tokens` - Token 定义文件

## 测试文件

测试文件分别存放在不同的目录中：

```
tests/
├── specific/
│   └── person_migration.smel          # Specific 版本测试
└── pauschalisiert/
    └── person_migration.smel_ps       # Pauschalisiert 版本测试
```

## 论文使用

这两种语法设计用于硕士论文中的对比研究：

1. **SMEL_Specific.g4** - 代表具体化、明确化的设计理念
2. **SMEL_Pauschalisiert.g4** - 代表通用化、参数化的设计理念

通过对比分析：
- 关键字数量
- 语法复杂度
- 可读性
- 可扩展性
- 解析性能

来评估两种设计方案的优劣。

## 注意事项

1. **文件扩展名区分**:
   - Specific 版本使用 `.smel`
   - Pauschalisiert 版本使用 `.smel_ps`

2. **解析器选择**: 根据文件扩展名自动选择对应的解析器

3. **Header 部分**: 两个版本的 Header 部分完全相同，不需要区分

4. **子句语法**: FLATTEN, NEST 等操作的子句（如 `GENERATE KEY`, `ADD REFERENCE`）在两个版本中保持一致

## 完整操作对比

### ADD 操作族

| 操作 | Specific | Pauschalisiert |
|------|----------|----------------|
| 添加属性 | `ADD_ATTRIBUTE` | `ADD_PS ATTRIBUTE` |
| 添加引用 | `ADD_REFERENCE` | `ADD_PS REFERENCE` |
| 添加嵌入 | `ADD_EMBEDDED` | `ADD_PS EMBEDDED` |
| 添加实体 | `ADD_ENTITY` | `ADD_PS ENTITY` |
| 添加主键 | `ADD_PRIMARY_KEY` | `ADD_PS PRIMARY KEY` |
| 添加外键 | `ADD_FOREIGN_KEY` | `ADD_PS FOREIGN KEY` |
| 添加唯一键 | `ADD_UNIQUE_KEY` | `ADD_PS UNIQUE KEY` |

### DELETE 操作族

| 操作 | Specific | Pauschalisiert |
|------|----------|----------------|
| 删除属性 | `DELETE_ATTRIBUTE` | `DELETE_PS ATTRIBUTE` |
| 删除引用 | `DELETE_REFERENCE` | `DELETE_PS REFERENCE` |
| 删除嵌入 | `DELETE_EMBEDDED` | `DELETE_PS EMBEDDED` |
| 删除实体 | `DELETE_ENTITY` | `DELETE_PS ENTITY` |

### 结构操作

| 操作 | Specific | Pauschalisiert |
|------|----------|----------------|
| FLATTEN | `FLATTEN` | `FLATTEN_PS` |
| NEST | `NEST` | `NEST_PS` |
| UNNEST | `UNNEST` | `UNNEST_PS` |
| EXTRACT | `EXTRACT` | `EXTRACT_PS` |

### 简单操作

| 操作 | Specific | Pauschalisiert |
|------|----------|----------------|
| COPY | `COPY` | `COPY_PS` |
| MOVE | `MOVE` | `MOVE_PS` |
| CAST | `CAST` | `CAST_PS` |
| LINKING | `LINKING` | `LINKING_PS` |
