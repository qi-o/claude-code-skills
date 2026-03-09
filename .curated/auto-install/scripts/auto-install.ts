#!/usr/bin/env bun
import { spawn } from "child_process";
import { platform, arch } from "os";

type PackageManager = "apt-get" | "dnf" | "yum" | "brew" | "winget" | "choco" | "npm" | "pip";

interface CommandInfo {
  name: string;
  packages: Record<PackageManager, string>;
  description?: string;
}

// 命令到包的映射
const COMMAND_MAP: Record<string, CommandInfo> = {
  // 版本控制
  git: {
    name: "Git",
    description: "分布式版本控制系统",
    packages: {
      "apt-get": "git",
      dnf: "git",
      yum: "git",
      brew: "git",
      winget: "Git.Git",
      choco: "git",
      npm: "-",
      pip: "gitpython",
    },
  },

  // 网络工具
  curl: {
    name: "cURL",
    description: "命令行 URL 传输工具",
    packages: {
      "apt-get": "curl",
      dnf: "curl",
      yum: "curl",
      brew: "curl",
      winget: "cURL.cURL",
      choco: "curl",
      npm: "-",
      pip: "-",
    },
  },
  wget: {
    name: "Wget",
    description: "非交互式网络下载工具",
    packages: {
      "apt-get": "wget",
      dnf: "wget",
      yum: "wget",
      brew: "wget",
      winget: "GnuWin32.Wget",
      choco: "wget",
      npm: "-",
      pip: "-",
    },
  },

  // 压缩工具
  tar: {
    name: "tar",
    description: "磁带归档程序",
    packages: {
      "apt-get": "tar",
      dnf: "tar",
      yum: "tar",
      brew: "gnu-tar",
      winget: "7zip.7zip",
      choco: "7zip",
      npm: "-",
      pip: "-",
    },
  },
  zip: {
    name: "Zip",
    description: "ZIP 压缩工具",
    packages: {
      "apt-get": "zip",
      dnf: "zip",
      yum: "zip",
      brew: "zip",
      winget: "Zip.Zip",
      choco: "zip",
      npm: "-",
      pip: "-",
    },
  },
  unzip: {
    name: "UnZip",
    description: "ZIP 解压工具",
    packages: {
      "apt-get": "unzip",
      dnf: "unzip",
      yum: "unzip",
      brew: "unzip",
      winget: "Zip.Zip",
      choco: "unzip",
      npm: "-",
      pip: "-",
    },
  },

  // 文本处理
  grep: {
    name: "GNU Grep",
    description: "模式匹配工具",
    packages: {
      "apt-get": "grep",
      dnf: "grep",
      yum: "grep",
      brew: "grep",
      winget: "GnuWin32.Grep",
      choco: "grep",
      npm: "-",
      pip: "-",
    },
  },
  sed: {
    name: "GNU Sed",
    description: "流编辑器",
    packages: {
      "apt-get": "sed",
      dnf: "sed",
      yum: "sed",
      brew: "gnu-sed",
      winget: "GnuWin32.Sed",
      choco: "sed",
      npm: "-",
      pip: "-",
    },
  },
  awk: {
    name: "GNU Awk",
    description: "文本处理工具",
    packages: {
      "apt-get": "awk",
      dnf: "gawk",
      yum: "gawk",
      brew: "gawk",
      winget: "GnuWin32.Gawk",
      choco: "gawk",
      npm: "-",
      pip: "-",
    },
  },

  // 开发工具
  node: {
    name: "Node.js",
    description: "JavaScript 运行时",
    packages: {
      "apt-get": "nodejs",
      dnf: "nodejs",
      yum: "nodejs",
      brew: "node",
      winget: "OpenJS.NodeJS.LTS",
      choco: "nodejs",
      npm: "-",
      pip: "-",
    },
  },
  npm: {
    name: "npm",
    description: "Node.js 包管理器",
    packages: {
      "apt-get": "npm",
      dnf: "npm",
      yum: "npm",
      brew: "npm",
      winget: "OpenJS.NodeJS.LTS",
      choco: "nodejs",
      npm: "-",
      pip: "-",
    },
  },
  python: {
    name: "Python",
    description: "Python 编程语言",
    packages: {
      "apt-get": "python3",
      dnf: "python3",
      yum: "python3",
      brew: "python@3",
      winget: "Python.Python.3.11",
      choco: "python311",
      npm: "-",
      pip: "-",
    },
  },
  pip: {
    name: "pip",
    description: "Python 包管理器",
    packages: {
      "apt-get": "python3-pip",
      dnf: "python3-pip",
      yum: "python3-pip",
      brew: "pip",
      winget: "Python.Python.3.11",
      choco: "python311",
      npm: "-",
      pip: "-",
    },
  },
  python3: {
    name: "Python 3",
    description: "Python 编程语言",
    packages: {
      "apt-get": "python3",
      dnf: "python3",
      yum: "python3",
      brew: "python@3",
      winget: "Python.Python.3.11",
      choco: "python311",
      npm: "-",
      pip: "-",
    },
  },

  // 运行时
  java: {
    name: "Java",
    description: "Java 运行时",
    packages: {
      "apt-get": "default-jre",
      dnf: "java-17-openjdk",
      yum: "java-17-openjdk",
      brew: "openjdk",
      winget: "EclipseAdoptium.Temurin.17.JDK",
      choco: "openjdk17",
      npm: "-",
      pip: "-",
    },
  },
  go: {
    name: "Go",
    description: "Go 编程语言",
    packages: {
      "apt-get": "golang",
      dnf: "golang",
      yum: "golang",
      brew: "go",
      winget: "GoLang.Go",
      choco: "go",
      npm: "-",
      pip: "-",
    },
  },
  rustc: {
    name: "Rust",
    description: "Rust 编程语言",
    packages: {
      "apt-get": "rustc",
      dnf: "rust",
      yum: "rust",
      brew: "rust",
      winget: "Rustlang.Rust.MSVC",
      choco: "rust",
      npm: "-",
      pip: "-",
    },
  },

  // 工具
  make: {
    name: "Make",
    description: "构建工具",
    packages: {
      "apt-get": "make",
      dnf: "make",
      yum: "make",
      brew: "make",
      winget: "GnuWin32.Make",
      choco: "make",
      npm: "-",
      pip: "-",
    },
  },
  cmake: {
    name: "CMake",
    description: "跨平台构建系统",
    packages: {
      "apt-get": "cmake",
      dnf: "cmake",
      yum: "cmake",
      brew: "cmake",
      winget: "Kitware.CMake",
      choco: "cmake",
      npm: "-",
      pip: "-",
    },
  },
  docker: {
    name: "Docker",
    description: "容器平台",
    packages: {
      "apt-get": "docker.io",
      dnf: "docker-ce",
      yum: "docker-ce",
      brew: "docker",
      winget: "Docker.DockerDesktop",
      choco: "docker-desktop",
      npm: "-",
      pip: "-",
    },
  },

  // 实用工具
  tree: {
    name: "Tree",
    description: "目录树状显示",
    packages: {
      "apt-get": "tree",
      dnf: "tree",
      yum: "tree",
      brew: "tree",
      winget: "GnuWin32.Tree",
      choco: "tree",
      npm: "-",
      pip: "-",
    },
  },
  htop: {
    name: "htop",
    description: "交互式进程查看器",
    packages: {
      "apt-get": "htop",
      dnf: "htop",
      yum: "htop",
      brew: "htop",
      winget: "oguaver.htop",
      choco: "htop",
      npm: "-",
      pip: "-",
    },
  },
  rsync: {
    name: "rsync",
    description: "远程同步工具",
    packages: {
      "apt-get": "rsync",
      dnf: "rsync",
      yum: "rsync",
      brew: "rsync",
      winget: "JW-Cohen.rsync",
      choco: "rsync",
      npm: "-",
      pip: "-",
    },
  },
  ffmpeg: {
    name: "FFmpeg",
    description: "音视频处理工具",
    packages: {
      "apt-get": "ffmpeg",
      dnf: "ffmpeg",
      yum: "ffmpeg",
      brew: "ffmpeg",
      winget: "FFmpeg.FFmpeg",
      choco: "ffmpeg",
      npm: "-",
      pip: "-",
    },
  },
  imagemagick: {
    name: "ImageMagick",
    description: "图像处理工具",
    packages: {
      "apt-get": "imagemagick",
      dnf: "ImageMagick",
      yum: "ImageMagick",
      brew: "imagemagick",
      winget: "ImageMagick.ImageMagick",
      choco: "imagemagick",
      npm: "-",
      pip: "-",
    },
  },
  convert: {
    name: "ImageMagick (convert)",
    description: "图像格式转换工具",
    packages: {
      "apt-get": "imagemagick",
      dnf: "ImageMagick",
      yum: "ImageMagick",
      brew: "imagemagick",
      winget: "ImageMagick.ImageMagick",
      choco: "imagemagick",
      npm: "-",
      pip: "-",
    },
  },

  // Git 工具
  gh: {
    name: "GitHub CLI",
    description: "GitHub 命令行工具",
    packages: {
      "apt-get": "gh",
      dnf: "gh",
      yum: "gh",
      brew: "gh",
      winget: "GitHub.GitHubCLI",
      choco: "gh",
      npm: "-",
      pip: "-",
    },
  },

  // SSH
  ssh: {
    name: "OpenSSH",
    description: "SSH 客户端",
    packages: {
      "apt-get": "openssh-client",
      dnf: "openssh-clients",
      yum: "openssh-clients",
      brew: "openssh",
      winget: "OpenSSH.OpenSSH",
      choco: "openssh",
      npm: "-",
      pip: "-",
    },
  },
  scp: {
    name: "OpenSSH (scp)",
    description: "安全复制工具",
    packages: {
      "apt-get": "openssh-client",
      dnf: "openssh-clients",
      yum: "openssh-clients",
      brew: "openssh",
      winget: "OpenSSH.OpenSSH",
      choco: "openssh",
      npm: "-",
      pip: "-",
    },
  },

  // 其他常用
  vim: {
    name: "Vim",
    description: "文本编辑器",
    packages: {
      "apt-get": "vim",
      dnf: "vim",
      yum: "vim",
      brew: "vim",
      winget: "vim.vim",
      choco: "vim",
      npm: "-",
      pip: "-",
    },
  },
  nano: {
    name: "Nano",
    description: "文本编辑器",
    packages: {
      "apt-get": "nano",
      dnf: "nano",
      yum: "nano",
      brew: "nano",
      winget: "GNU.Nano",
      choco: "nano",
      npm: "-",
      pip: "-",
    },
  },
  jq: {
    name: "jq",
    description: "JSON 处理工具",
    packages: {
      "apt-get": "jq",
      dnf: "jq",
      yum: "jq",
      brew: "jq",
      winget: "jq.jq",
      choco: "jq",
      npm: "-",
      pip: "-",
    },
  },
  yq: {
    name: "yq",
    description: "YAML 处理工具",
    packages: {
      "apt-get": "yq",
      dnf: "yq",
      yum: "yq",
      brew: "yq",
      winget: "mikefarah.yq",
      choco: "yq",
      npm: "-",
      pip: "-",
    },
  },
  tmux: {
    name: "Tmux",
    description: "终端复用器",
    packages: {
      "apt-get": "tmux",
      dnf: "tmux",
      yum: "tmux",
      brew: "tmux",
      winget: "tmux",
      choco: "tmux",
      npm: "-",
      pip: "-",
    },
  },
  wget: {
    name: "Wget",
    description: "非交互式网络下载工具",
    packages: {
      "apt-get": "wget",
      dnf: "wget",
      yum: "wget",
      brew: "wget",
      winget: "GnuWin32.Wget",
      choco: "wget",
      npm: "-",
      pip: "-",
    },
  },
  aria2c: {
    name: "aria2",
    description: "多协议下载工具",
    packages: {
      "apt-get": "aria2",
      dnf: "aria2",
      yum: "aria2",
      brew: "aria2",
      winget: "aria2.aria2",
      choco: "aria2",
      npm: "-",
      pip: "-",
    },
  },
  bun: {
    name: "Bun",
    description: "JavaScript 运行时",
    packages: {
      "apt-get": "-",
      dnf: "-",
      yum: "-",
      brew: "oven-sh/bun/bun",
      winget: "OvenSh.Bun",
      choco: "-",
      npm: "bun",
      pip: "-",
    },
  },
  deno: {
    name: "Deno",
    description: "JavaScript/TypeScript 运行时",
    packages: {
      "apt-get": "-",
      dnf: "deno",
      yum: "deno",
      brew: "deno",
      winget: "Deno.Deno",
      choco: "deno",
      npm: "deno",
      pip: "-",
    },
  },
};

function getPlatform(): NodeJS.Platform {
  return platform();
}

function detectPackageManager(preferred?: PackageManager): PackageManager | null {
  const plat = getPlatform();

  // 如果指定了包管理器，先检查是否可用
  if (preferred) {
    if (checkCommandAvailable(preferred)) {
      return preferred;
    }
    console.error(`指定的包管理器 ${preferred} 不可用`);
    return null;
  }

  // 检测系统包管理器
  if (plat === "win32") {
    if (checkCommandAvailable("winget")) return "winget";
    if (checkCommandAvailable("choco")) return "choco";
  } else if (plat === "darwin") {
    if (checkCommandAvailable("brew")) return "brew";
  } else {
    // Linux
    if (checkCommandAvailable("apt-get")) return "apt-get";
    if (checkCommandAvailable("dnf")) return "dnf";
    if (checkCommandAvailable("yum")) return "yum";
  }

  // 回退到 npm/pip
  if (checkCommandAvailable("npm")) return "npm";
  if (checkCommandAvailable("pip")) return "pip";

  return null;
}

function checkCommandAvailable(cmd: string): boolean {
  try {
    const isWindows = getPlatform() === "win32";
    const checkCmd = isWindows ? "where" : "which";
    const proc = spawn(checkCmd, [cmd], { stdio: "pipe" });
    return new Promise((resolve) => {
      proc.on("close", (code) => resolve(code === 0));
      proc.on("error", () => resolve(false));
    }) as unknown as boolean;
  } catch {
    return false;
  }
}

async function commandExists(cmd: string): Promise<boolean> {
  const isWindows = getPlatform() === "win32";
  const checkCmd = isWindows ? "where" : "which";
  return new Promise((resolve) => {
    const proc = spawn(checkCmd, [cmd], { stdio: "pipe" });
    proc.on("close", (code) => resolve(code === 0));
    proc.on("error", () => resolve(false));
  });
}

function getInstallCommand(packageManager: PackageManager, packageName: string): string {
  const plat = getPlatform();

  switch (packageManager) {
    case "apt-get":
      return `sudo apt-get update && sudo apt-get install -y ${packageName}`;
    case "dnf":
      return `sudo dnf install -y ${packageName}`;
    case "yum":
      return `sudo yum install -y ${packageName}`;
    case "brew":
      return `brew install ${packageName}`;
    case "winget":
      return `winget install --id ${packageName} --silent --accept-package-agreements --accept-source-agreements`;
    case "choco":
      return `choco install ${packageName} -y`;
    case "npm":
      return `npm install -g ${packageName}`;
    case "pip":
      return `pip install ${packageName}`;
    default:
      return "";
  }
}

function runCmd(cmd: string, args: string[]): Promise<{ code: number; stdout: string; stderr: string }> {
  return new Promise((resolve) => {
    const proc = spawn(cmd, args, { stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    proc.stdout?.on("data", (d) => (stdout += d.toString()));
    proc.stderr?.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => resolve({ code: code ?? 1, stdout, stderr }));
    proc.on("error", (e) => resolve({ code: 1, stdout: "", stderr: e.message }));
  });
}

function printHelp() {
  console.log(`Usage: bun auto-install.ts <command> [options]

Options:
  --package-manager <pm>  指定包管理器 (apt-get/dnf/yum/brew/winget/choco/npm/pip)
  --dry-run              模拟运行，不实际安装
  --json                 JSON 格式输出
  -h, --help             显示帮助`);
}

interface Options {
  command: string;
  packageManager?: PackageManager;
  dryRun: boolean;
  json: boolean;
}

function parseArgs(args: string[]): Options | null {
  const opts: Options = {
    command: "",
    dryRun: false,
    json: false,
  };

  const packageManagers: PackageManager[] = ["apt-get", "dnf", "yum", "brew", "winget", "choco", "npm", "pip"];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "-h" || arg === "--help") {
      printHelp();
      process.exit(0);
    } else if (arg === "--package-manager" || arg === "-pm") {
      const pm = args[++i] as PackageManager;
      if (!packageManagers.includes(pm)) {
        console.error(`无效的包管理器: ${pm}`);
        return null;
      }
      opts.packageManager = pm;
    } else if (arg === "--dry-run") {
      opts.dryRun = true;
    } else if (arg === "--json") {
      opts.json = true;
    } else if (!arg.startsWith("-")) {
      opts.command = arg;
    }
  }

  if (!opts.command) {
    console.error("错误: 需要指定要安装的命令");
    printHelp();
    return null;
  }

  return opts;
}

interface Result {
  command: string;
  packageManager: PackageManager | null;
  packageName: string;
  installCommand: string;
  success: boolean;
  error?: string;
}

async function main() {
  const args = process.argv.slice(2);
  const opts = parseArgs(args);
  if (!opts) process.exit(1);

  const cmd = opts.command.toLowerCase();

  // 检查命令是否已安装
  if (await commandExists(cmd)) {
    const result: Result = {
      command: cmd,
      packageManager: null,
      packageName: "",
      installCommand: "",
      success: true,
    };
    if (opts.json) {
      console.log(JSON.stringify({ ...result, message: "命令已安装" }, null, 2));
    } else {
      console.log(`命令 '${cmd}' 已安装`);
    }
    return;
  }

  // 查找命令信息
  const cmdInfo = COMMAND_MAP[cmd];

  // 检测包管理器
  const packageManager = detectPackageManager(opts.packageManager);

  if (!packageManager) {
    const result: Result = {
      command: cmd,
      packageManager: null,
      packageName: cmdInfo?.packages[opts.packageManager as PackageManager] || cmd,
      installCommand: "",
      success: false,
      error: "未找到可用的包管理器",
    };
    if (opts.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error("错误: 未找到可用的包管理器 (winget/choco/brew/apt-get/dnf/yum/npm/pip)");
    }
    process.exit(1);
  }

  // 获取包名
  const packageName = cmdInfo?.packages[packageManager];

  if (!packageName || packageName === "-") {
    const result: Result = {
      command: cmd,
      packageManager,
      packageName: cmd,
      installCommand: "",
      success: false,
      error: `命令 '${cmd}' 不支持通过 ${packageManager} 安装`,
    };
    if (opts.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error(`错误: 命令 '${cmd}' 不支持通过 ${packageManager} 安装`);
    }
    process.exit(1);
  }

  // 生成安装命令
  const installCommand = getInstallCommand(packageManager, packageName);

  // 模拟运行
  if (opts.dryRun) {
    const result: Result = {
      command: cmd,
      packageManager,
      packageName,
      installCommand,
      success: true,
    };
    if (opts.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(`[Dry Run] 命令: ${cmd}`);
      console.log(`[Dry Run] 包管理器: ${packageManager}`);
      console.log(`[Dry Run] 包名: ${packageName}`);
      console.log(`[Dry Run] 安装命令: ${installCommand}`);
    }
    return;
  }

  // 执行安装
  if (opts.json) {
    console.log(JSON.stringify({
      command: cmd,
      packageManager,
      packageName,
      installCommand,
      message: "正在安装...",
    }, null, 2));
  } else {
    console.log(`正在安装 '${cmd}' 使用 ${packageManager}...`);
    console.log(`安装命令: ${installCommand}`);
  }

  const isWindows = getPlatform() === "win32";
  const installCmd = isWindows ? installCommand.split(" ")[0] : installCommand.split(" ")[0];
  const installArgs = isWindows ? installCommand.split(" ").slice(1) : installCommand.split(" ").slice(1);

  // 对于需要 sudo 的命令
  let finalCmd = installCommand;
  if (!isWindows && packageManager !== "brew" && packageManager !== "npm" && packageManager !== "pip") {
    // 检查是否需要 sudo
    const sudoCheck = await runCmd("id", ["-u"]);
    const needsSudo = sudoCheck.code !== 0;
    if (needsSudo) {
      finalCmd = "sudo " + installCommand;
    }
  }

  // 解析命令和参数
  const cmdParts = finalCmd.split(" ");
  const actualCmd = cmdParts[0];
  const actualArgs = cmdParts.slice(1);

  const { code, stdout, stderr } = await runCmd(actualCmd, actualArgs);

  const result: Result = {
    command: cmd,
    packageManager,
    packageName,
    installCommand,
    success: code === 0,
    error: code !== 0 ? stderr : undefined,
  };

  if (opts.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    if (code === 0) {
      console.log(`成功安装 '${cmd}'`);

      // 验证安装
      if (await commandExists(cmd)) {
        console.log(`验证成功: '${cmd}' 已可用`);
      } else {
        console.warn(`警告: 安装完成但无法验证命令可用性，可能需要重启终端`);
      }
    } else {
      console.error(`安装失败: ${stderr}`);
      process.exit(1);
    }
  }
}

main();
