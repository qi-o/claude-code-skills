#!/usr/bin/env bun

/**
 * Agent Self-Heal - 错误诊断与修复工具
 *
 * 用法:
 *   bun self-heal.ts <error-message> [options]
 *   bun self-heal.ts --report [options]
 *
 * 选项:
 *   --auto-fix, -a    尝试自动修复
 *   --report, -r      生成诊断报告
 *   --json            JSON 格式输出
 *   --context, -c     附加上下文信息
 */

interface ErrorAnalysis {
  type: string;
  category: string;
  severity: "critical" | "warning" | "info";
  possibleCauses: string[];
  fixSuggestions: FixSuggestion[];
  autoFixable: boolean;
}

interface FixSuggestion {
  action: string;
  command?: string;
  priority: "high" | "medium" | "low";
}

// 错误模式匹配规则
const ERROR_PATTERNS: Array<{
  pattern: RegExp;
  category: string;
  type: string;
  severity: "critical" | "warning" | "info";
  possibleCauses: string[];
  fixSuggestions: FixSuggestion[];
  autoFixable: boolean;
}> = [
  // ===== 1. 文件相关错误 =====
  {
    pattern: /ENOENT: no such file or directory|Cannot find file|The system cannot find the file specified/,
    category: "文件错误",
    type: "FileNotFound",
    severity: "warning",
    possibleCauses: [
      "文件路径拼写错误",
      "文件尚未创建",
      "工作目录不正确",
      "相对路径 vs 绝对路径混淆"
    ],
    fixSuggestions: [
      {
        action: "检查文件路径是否正确（大小写敏感）",
        command: "ls -la <directory>",
        priority: "high"
      },
      {
        action: "确认当前工作目录",
        command: "pwd",
        priority: "high"
      },
      {
        action: "使用绝对路径尝试",
        command: "realpath <path>",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /ENOENT: no such file or directory.*mkdir|Cannot create directory/,
    category: "文件错误",
    type: "DirectoryNotFound",
    severity: "warning",
    possibleCauses: [
      "父目录不存在",
      "路径中包含非法字符"
    ],
    fixSuggestions: [
      {
        action: "创建目录及父目录",
        command: "mkdir -p <path>",
        priority: "high"
      }
    ],
    autoFixable: true
  },
  {
    pattern: /EEXIST: file already exists|File already exists/,
    category: "文件错误",
    type: "FileAlreadyExists",
    severity: "info",
    possibleCauses: [
      "尝试创建已存在的文件",
      "未指定覆盖选项"
    ],
    fixSuggestions: [
      {
        action: "使用 --force 覆盖",
        command: "<command> --force",
        priority: "high"
      },
      {
        action: "先删除再创建",
        command: "rm <file> && <command>",
        priority: "medium"
      }
    ],
    autoFixable: true
  },

  // ===== 2. 权限相关错误 =====
  {
    pattern: /EACCES: permission denied|Permission denied: /,
    category: "权限错误",
    type: "PermissionDenied",
    severity: "critical",
    possibleCauses: [
      "当前用户无读取/写入/执行权限",
      "文件/目录由其他用户拥有",
      "缺少目录执行权限"
    ],
    fixSuggestions: [
      {
        action: "修复文件权限 (Linux/macOS)",
        command: "chmod 755 <path>",
        priority: "high"
      },
      {
        action: "获得文件所有权",
        command: "sudo chown -R $(whoami) <path>",
        priority: "high"
      },
      {
        action: "Windows: 管理员权限运行",
        command: "以管理员身份运行终端",
        priority: "high"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /EPERM: operation not permitted|Operation not permitted/,
    category: "权限错误",
    type: "OperationNotPermitted",
    severity: "critical",
    possibleCauses: [
      "系统保护的文件",
      "防病毒软件阻止",
      "文件被其他进程锁定"
    ],
    fixSuggestions: [
      {
        action: "关闭可能锁定文件的程序",
        priority: "high"
      },
      {
        action: "检查防病毒设置",
        priority: "medium"
      },
      {
        action: "使用管理员权限",
        priority: "high"
      }
    ],
    autoFixable: false
  },

  // ===== 3. 模块/依赖错误 =====
  {
    pattern: /Cannot find module|ERR_MODULE_NOT_FOUND|Cannot resolve module/,
    category: "模块错误",
    type: "ModuleNotFound",
    severity: "warning",
    possibleCauses: [
      "模块未安装",
      "模块路径错误（缺少扩展名）",
      "node_modules 问题",
      "TypeScript 路径映射错误"
    ],
    fixSuggestions: [
      {
        action: "确认文件扩展名 (.ts, .js, .tsx, .jsx)",
        priority: "high"
      },
      {
        action: "检查 package.json 是否包含该依赖",
        priority: "high"
      },
      {
        action: "安装缺失的模块",
        command: "npm install <module-name>",
        priority: "high"
      },
      {
        action: "删除 node_modules 重新安装",
        command: "rm -rf node_modules && npm install",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /ERR_PACKAGE_PATH_NOT_EXPORTED|Module has no default export/,
    category: "模块错误",
    type: "ModuleExportError",
    severity: "warning",
    possibleCauses: [
      "模块导出方式不匹配",
      "package.json exports 字段配置错误"
    ],
    fixSuggestions: [
      {
        action: "检查导入方式 (default vs named export)",
        priority: "high"
      },
      {
        action: "检查 package.json exports 字段",
        priority: "medium"
      },
      {
        action: "更新模块版本",
        command: "npm install <package>@latest",
        priority: "medium"
      }
    ],
    autoFixable: false
  },

  // ===== 4. 语法错误 =====
  {
    pattern: /SyntaxError: Unexpected token|SyntaxError: Unexpected string|SyntaxError: Unexpected number/,
    category: "语法错误",
    type: "SyntaxError",
    severity: "critical",
    possibleCauses: [
      "括号/引号不匹配",
      "缺少分号或逗号",
      "错误的转义字符",
      "JSX 语法错误"
    ],
    fixSuggestions: [
      {
        action: "检查错误行号的语法",
        priority: "high"
      },
      {
        action: "确认括号和引号配对",
        priority: "high"
      },
      {
        action: "检查是否有尾随逗号",
        priority: "medium"
      },
      {
        action: "使用 Prettier 格式化代码",
        command: "npx prettier --write <file>",
        priority: "low"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /JSON Parse Error|Unexpected end of JSON/,
    category: "语法错误",
    type: "JSONParseError",
    severity: "critical",
    possibleCauses: [
      "JSON 末尾多余逗号",
      "键名未用双引号",
      "存在单引号或注释"
    ],
    fixSuggestions: [
      {
        action: "验证 JSON 格式",
        command: "node -e \"JSON.parse(fs.readFileSync('file.json'))\"",
        priority: "high"
      },
      {
        action: "检查并修复 JSON 语法",
        priority: "high"
      }
    ],
    autoFixable: false
  },

  // ===== 5. 类型错误 =====
  {
    pattern: /TypeError: Cannot read (property|properties) of (undefined|null)|undefined is not an object|Cannot read property/,
    category: "类型错误",
    type: "TypeErrorUndefined",
    severity: "critical",
    possibleCauses: [
      "访问了 undefined/null 的属性",
      "异步操作返回前就访问",
      "函数返回值可能为 undefined"
    ],
    fixSuggestions: [
      {
        action: "使用可选链 (?.)",
        priority: "high"
      },
      {
        action: "使用空值合并 (??)",
        priority: "high"
      },
      {
        action: "添加空值检查",
        priority: "high"
      },
      {
        action: "使用默认参数",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /TypeError: .* is not a function|TypeError: .* is not a constructor/,
    category: "类型错误",
    type: "TypeErrorNotFunction",
    severity: "critical",
    possibleCauses: [
      "变量赋值错误",
      "导入方式错误",
      "方法未绑定 this"
    ],
    fixSuggestions: [
      {
        action: "检查导入方式是否正确",
        priority: "high"
      },
      {
        action: "检查是否需要绑定 this",
        priority: "high"
      },
      {
        action: "确认构造函数使用正确",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /TypeError: .* is not iterable/,
    category: "类型错误",
    type: "TypeErrorNotIterable",
    severity: "critical",
    possibleCauses: [
      "尝试遍历非可迭代对象",
      "解构了 null/undefined"
    ],
    fixSuggestions: [
      {
        action: "确认对象是否可迭代",
        priority: "high"
      },
      {
        action: "使用 Object.values() 或 Object.entries()",
        priority: "medium"
      },
      {
        action: "添加空值检查",
        priority: "high"
      }
    ],
    autoFixable: false
  },

  // ===== 6. 网络错误 =====
  {
    pattern: /ECONNREFUSED|Connection refused/,
    category: "网络错误",
    type: "ConnectionRefused",
    severity: "warning",
    possibleCauses: [
      "服务器未运行",
      "端口错误",
      "防火墙阻止"
    ],
    fixSuggestions: [
      {
        action: "确认服务器是否运行",
        priority: "high"
      },
      {
        action: "检查端口号是否正确",
        priority: "high"
      },
      {
        action: "测试连接",
        command: "curl -v <url>",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /ETIMEDOUT|Connection timed out/,
    category: "网络错误",
    type: "ConnectionTimeout",
    severity: "warning",
    possibleCauses: [
      "网络延迟过高",
      "服务器响应慢",
      "网络不稳定"
    ],
    fixSuggestions: [
      {
        action: "增加超时时间",
        priority: "high"
      },
      {
        action: "使用 http-retry 实现重试",
        priority: "medium"
      },
      {
        action: "检查网络连接",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /ENOTFOUND|DNS lookup failed|getaddrinfo/,
    category: "网络错误",
    type: "DNSError",
    severity: "warning",
    possibleCauses: [
      "URL 拼写错误",
      "DNS 配置问题",
      "网络未连接"
    ],
    fixSuggestions: [
      {
        action: "确认 URL 拼写正确",
        priority: "high"
      },
      {
        action: "测试 DNS 解析",
        command: "nslookup <host>",
        priority: "medium"
      },
      {
        action: "刷新 DNS 缓存",
        command: "ipconfig /flushdns (Windows)",
        priority: "low"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /fetch failed|Network request failed/,
    category: "网络错误",
    type: "NetworkRequestFailed",
    severity: "warning",
    possibleCauses: [
      "请求失败（4xx/5xx 状态码）",
      "网络问题",
      "CORS 错误"
    ],
    fixSuggestions: [
      {
        action: "检查 HTTP 状态码",
        priority: "high"
      },
      {
        action: "查看服务器响应",
        priority: "high"
      },
      {
        action: "添加重试机制",
        priority: "medium"
      },
      {
        action: "检查 CORS 配置",
        priority: "medium"
      }
    ],
    autoFixable: false
  },

  // ===== 7. 进程/环境错误 =====
  {
    pattern: /Process exited with code 137|Exit code 137/,
    category: "进程错误",
    type: "OOMKilled",
    severity: "critical",
    possibleCauses: [
      "内存不足 (OOM Killer)",
      "进程被系统终止"
    ],
    fixSuggestions: [
      {
        action: "增加 Node.js 内存限制",
        command: "node --max-old-space-size=4096 <script>",
        priority: "high"
      },
      {
        action: "检查代码是否有内存泄漏",
        priority: "high"
      },
      {
        action: "使用流处理大数据",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /UnhandledPromiseRejection|Promise rejection/,
    category: "异步错误",
    type: "UnhandledRejection",
    severity: "warning",
    possibleCauses: [
      "async 函数未 await",
      "Promise 未 .catch()"
    ],
    fixSuggestions: [
      {
        action: "添加 .catch() 处理",
        priority: "high"
      },
      {
        action: "使用 try-catch 包装 await",
        priority: "high"
      },
      {
        action: "添加全局 unhandledRejection 处理",
        command: "process.on('unhandledRejection', handler)",
        priority: "medium"
      }
    ],
    autoFixable: false
  },
  {
    pattern: /command not found|Command not found/,
    category: "环境错误",
    type: "CommandNotFound",
    severity: "warning",
    possibleCauses: [
      "命令未安装",
      "PATH 环境变量未配置"
    ],
    fixSuggestions: [
      {
        action: "确认命令已安装",
        priority: "high"
      },
      {
        action: "检查 PATH 环境变量",
        command: "echo $PATH",
        priority: "high"
      },
      {
        action: "安装缺失的命令",
        command: "npm install -g <package>",
        priority: "high"
      }
    ],
    autoFixable: false
  }
];

/**
 * 分析错误信息
 */
function analyzeError(errorMessage: string): ErrorAnalysis {
  // 遍历所有错误模式，找到第一个匹配的
  for (const rule of ERROR_PATTERNS) {
    if (rule.pattern.test(errorMessage)) {
      return {
        type: rule.type,
        category: rule.category,
        severity: rule.severity,
        possibleCauses: rule.possibleCauses,
        fixSuggestions: rule.fixSuggestions,
        autoFixable: rule.autoFixable
      };
    }
  }

  // 未匹配到任何模式，返回通用分析
  return {
    type: "Unknown",
    category: "未知错误",
    severity: "info",
    possibleCauses: [
      "未知错误类型",
      "需要更多上下文信息"
    ],
    fixSuggestions: [
      {
        action: "查看完整错误堆栈",
        priority: "high"
      },
      {
        action: "提供更多错误上下文",
        priority: "medium"
      }
    ],
    autoFixable: false
  };
}

/**
 * 生成诊断报告
 */
function generateReport(errorMessage: string, context: string = "", json: boolean = false): void {
  const analysis = analyzeError(errorMessage);

  if (json) {
    console.log(JSON.stringify({
      errorMessage,
      context,
      analysis,
      timestamp: new Date().toISOString()
    }, null, 2));
    return;
  }

  // 人类可读格式
  console.log("\n" + "=".repeat(60));
  console.log("🔍 Agent Self-Heal 诊断报告");
  console.log("=".repeat(60));

  console.log("\n📋 错误信息:");
  console.log(`   ${errorMessage}`);

  if (context) {
    console.log("\n📎 上下文:");
    console.log(`   ${context}`);
  }

  console.log("\n📊 分析结果:");
  console.log(`   类型: ${analysis.type}`);
  console.log(`   类别: ${analysis.category}`);
  console.log(`   严重程度: ${getSeverityEmoji(analysis.severity)} ${analysis.severity}`);

  console.log("\n🔎 可能原因:");
  analysis.possibleCauses.forEach((cause, index) => {
    console.log(`   ${index + 1}. ${cause}`);
  });

  console.log("\n🛠️ 建议操作:");
  const sortedSuggestions = [...analysis.fixSuggestions].sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  sortedSuggestions.forEach((suggestion, index) => {
    const priorityIcon = suggestion.priority === "high" ? "🔴" : suggestion.priority === "medium" ? "🟡" : "🟢";
    console.log(`   ${priorityIcon} ${suggestion.action}`);
    if (suggestion.command) {
      console.log(`      命令: ${suggestion.command}`);
    }
  });

  if (analysis.autoFixable) {
    console.log("\n✨ 此错误可自动修复");
  } else {
    console.log("\n⚠️ 此错误需要手动修复");
  }

  console.log("\n" + "=".repeat(60));
}

/**
 * 获取严重程度表情
 */
function getSeverityEmoji(severity: string): string {
  switch (severity) {
    case "critical":
      return "🔴";
    case "warning":
      return "🟡";
    case "info":
      return "🔵";
    default:
      return "⚪";
  }
}

/**
 * 执行自动修复
 */
async function attemptAutoFix(analysis: ErrorAnalysis): Promise<void> {
  console.log("\n⚡ 尝试自动修复...");

  const highPriorityFixes = analysis.fixSuggestions.filter(s => s.priority === "high" && s.command);

  for (const fix of highPriorityFixes) {
    if (fix.command) {
      console.log(`\n▶️ 执行: ${fix.command}`);
      try {
        const { spawn } = await import("child_process");
        const [cmd, ...args] = fix.command.split(" ");
        const child = spawn(cmd, args, { shell: true });

        child.stdout.on("data", (data) => {
          console.log(data.toString());
        });

        child.stderr.on("data", (data) => {
          console.error(data.toString());
        });

        await new Promise<void>((resolve) => {
          child.on("close", (code) => {
            if (code === 0) {
              console.log(`✅ 成功执行: ${fix.action}`);
            } else {
              console.log(`⚠️ 命令执行失败，退出码: ${code}`);
            }
            resolve();
          });
        });
      } catch (error) {
        console.log(`❌ 无法执行命令: ${fix.command}`);
      }
    }
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);

  // 解析参数
  let errorMessage = "";
  let context = "";
  let autoFix = false;
  let generateReportOnly = false;
  let jsonOutput = false;

  const flags = ["--auto-fix", "-a", "--report", "-r", "--json", "-c", "--context"];
  const processedFlags = new Set<string>();

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if ((arg === "-c" || arg === "--context") && nextArg && !flags.includes(nextArg)) {
      context = nextArg;
      processedFlags.add(arg);
      processedFlags.add(nextArg);
      i++;
    } else if (!flags.includes(arg) && !arg.startsWith("-") && !processedFlags.has(arg)) {
      errorMessage = arg;
    } else if (arg === "--auto-fix" || arg === "-a") {
      autoFix = true;
      processedFlags.add(arg);
    } else if (arg === "--report" || arg === "-r") {
      generateReportOnly = true;
      processedFlags.add(arg);
    } else if (arg === "--json") {
      jsonOutput = true;
      processedFlags.add(arg);
    }
  }

  if (generateReportOnly) {
    // 生成通用诊断报告
    if (jsonOutput) {
      console.log(JSON.stringify({
        status: "ok",
        timestamp: new Date().toISOString(),
        message: "Self-Heal 诊断工具就绪"
      }, null, 2));
    } else {
      console.log("\n" + "=".repeat(60));
      console.log("🔧 Agent Self-Heal 工具就绪");
      console.log("=".repeat(60));
      console.log("\n用法:");
      console.log("  bun self-heal.ts <错误信息> [options]");
      console.log("  bun self-heal.ts --report");
      console.log("\n选项:");
      console.log("  --auto-fix, -a    尝试自动修复");
      console.log("  --report, -r      生成诊断报告");
      console.log("  --json            JSON 格式输出");
      console.log("  --context, -c     附加上下文");
      console.log("\n触发词: self-heal, 自检, debug, 诊断, error analysis");
      console.log("=".repeat(60));
    }
    return;
  }

  if (!errorMessage) {
    console.error("❌ 请提供错误信息");
    console.log("用法: bun self-heal.ts <错误信息> [options]");
    process.exit(1);
  }

  const analysis = analyzeError(errorMessage);
  generateReport(errorMessage, context, jsonOutput);

  if (autoFix && analysis.autoFixable) {
    await attemptAutoFix(analysis);
  }
}

main().catch(console.error);
