/**
 * 漫画生成脚本 - 使用兔子 API (tu-zi.com)
 * 支持 gemini-3-pro-image-preview (nano banana 2) 模型
 * 
 * 使用方法:
 *   export TUZI_API_KEY=sk-xxx
 *   npx tsx generate_manga.ts --prompt "你的提示词"
 */

import OpenAI from "openai";
import { writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";
import path from "path";

// ====================================
// 配置参数
// ====================================
const API_BASE = "https://api.tu-zi.com/v1";
const MODEL_NAME = "gemini-3-pro-image-preview";  // nano banana 2, 生成质量 1k

/**
 * 漫画生成选项接口
 */
interface GenerateOptions {
  page: number;          // 页码
  prompt: string;        // 提示词
  outputDir?: string;    // 输出目录，默认 ./output
}

/**
 * 保存二进制文件到磁盘
 */
async function saveBinaryFile(fileName: string, content: Buffer): Promise<void> {
  try {
    await writeFile(fileName, content);
    console.log(`✅ 图片已保存: ${fileName}`);
  } catch (err) {
    console.error(`❌ 保存文件失败 ${fileName}:`, err);
    throw err;
  }
}

/**
 * 从 URL 下载图片
 */
async function downloadImage(url: string, fileName: string): Promise<void> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const buffer = Buffer.from(await response.arrayBuffer());
    await saveBinaryFile(fileName, buffer);
  } catch (err) {
    console.error(`❌ 下载图片失败:`, err);
    throw err;
  }
}

/**
 * 生成单页漫画图片 - 使用 images.generate 端点
 */
async function generateMangaPage(options: GenerateOptions): Promise<string[]> {
  const { page, prompt, outputDir = "./output" } = options;

  // 确保输出目录存在
  if (!existsSync(outputDir)) {
    await mkdir(outputDir, { recursive: true });
    console.log(`📁 创建输出目录: ${outputDir}`);
  }

  console.log(`\n🎨 正在生成第 ${page} 页漫画...`);
  console.log(`📝 提示词: ${prompt.substring(0, 100)}${prompt.length > 100 ? '...' : ''}`);

  // 获取 API Key
  const apiKey = "sk-fazTLv940n39kP9M4mf02kZGqy0AxKfOk9DGttkoioEAx5KV"
  if (!apiKey) {
    console.error("❌ 请设置环境变量 TUZI_API_KEY 或 GEMINI_API_KEY");
    throw new Error("API Key 未设置");
  }

  // 初始化 OpenAI 兼容客户端
  const client = new OpenAI({
    baseURL: API_BASE,
    apiKey: apiKey,
  });

  console.log(`🚀 发送生成请求到 ${API_BASE}...`);
  console.log(`📦 使用模型: ${MODEL_NAME}`);

  try {
    // 使用 images.generate 端点
    const result = await client.images.generate({
      model: MODEL_NAME,
      prompt: prompt,
    });

    console.log("✨ API 响应成功!");

    const savedFiles: string[] = [];

    // 处理返回的图片数据
    if (result.data && result.data.length > 0) {
      for (let i = 0; i < result.data.length; i++) {
        const imageData = result.data[i];
        const fileName = path.join(
          outputDir,
          `manga_page_${String(page).padStart(2, "0")}${i > 0 ? `_${i}` : ""}.png`
        );

        // 优先使用 base64 数据
        if (imageData.b64_json) {
          console.log(`📷 接收到 base64 图片数据`);
          const buffer = Buffer.from(imageData.b64_json, "base64");
          await saveBinaryFile(fileName, buffer);
          savedFiles.push(fileName);
        } 
        // 其次使用 URL
        else if (imageData.url) {
          console.log(`🔗 接收到图片 URL: ${imageData.url.substring(0, 50)}...`);
          await downloadImage(imageData.url, fileName);
          savedFiles.push(fileName);
        }
      }
    }

    if (savedFiles.length === 0) {
      console.warn("⚠️ 未能获取到图片");
    } else {
      console.log(`\n✨ 成功生成 ${savedFiles.length} 张图片!`);
    }

    return savedFiles;

  } catch (error: unknown) {
    const err = error as Error & { status?: number; message?: string };
    console.error("\n❌ 生成失败:", err.message || error);
    
    if (err.status === 429) {
      console.error("💡 提示: API 配额超限，请稍后重试");
    } else if (err.status === 401) {
      console.error("💡 提示: API Key 无效，请检查");
    }
    
    throw error;
  }
}

/**
 * 批量生成多页漫画
 */
async function generateMangaBook(
  pages: Array<{ page: number; prompt: string }>,
  outputDir?: string
): Promise<string[]> {
  const results: string[] = [];

  console.log(`\n📚 开始批量生成 ${pages.length} 页漫画...`);

  for (let i = 0; i < pages.length; i++) {
    const pageData = pages[i];
    try {
      console.log(`\n[${i + 1}/${pages.length}] 处理中...`);
      const files = await generateMangaPage({
        ...pageData,
        outputDir,
      });
      results.push(...files);

      // 添加延迟避免 API 限流
      if (i < pages.length - 1) {
        console.log("⏳ 等待 2 秒后生成下一页...");
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    } catch (error) {
      console.error(`❌ 第 ${pageData.page} 页生成失败:`, error);
    }
  }

  console.log(`\n📊 生成完成! 共生成 ${results.length} 张图片`);
  return results;
}

/**
 * CLI 入口函数
 */
async function main() {
  const args = process.argv.slice(2);

  // 解析命令行参数
  let page = 1;
  let prompt = "";
  let outputDir = "./output";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--page" && args[i + 1]) {
      page = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === "--prompt" && args[i + 1]) {
      prompt = args[i + 1];
      i++;
    } else if (args[i] === "--output" && args[i + 1]) {
      outputDir = args[i + 1];
      i++;
    }
  }

  if (!prompt) {
    // 示例提示词
    prompt = `生成一张漫画学习页面图片。
场景：教室里，黑板前
角色：
- 哆啦A梦：蓝色机器猫，圆圆的身体，戴着铃铛，拿着教鞭指向黑板
- 大雄：戴眼镜的小男孩，坐在课桌前，好奇地看着黑板
对话气泡：
- 哆啦A梦："今天我们来学习人工智能的基础知识！"
- 大雄："人工智能是什么呢？"
画面元素：黑板上写着"AI 入门"，教室里有阳光透过窗户照进来
要求：日式漫画风格，线条清晰，色彩明快`;

    console.log("📌 未提供提示词，使用示例提示词");
  }

  try {
    await generateMangaPage({ page, prompt, outputDir });
  } catch (error: unknown) {
    const err = error as Error;
    console.error("\n生成图片错误:", err.message || error);
    process.exit(1);
  }
}

// 导出函数供其他模块使用
export { generateMangaPage, generateMangaBook, GenerateOptions };

// 运行主函数
main().catch(console.error);
