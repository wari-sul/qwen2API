import os
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FRONTEND_SRC_DIR = os.path.join(ROOT_DIR, "frontend", "src")
REQUIREMENTS_FILE = os.path.join(ROOT_DIR, "backend", "requirements.txt")
README_FILE = os.path.join(ROOT_DIR, "README.md")
TEMPLATE_README = os.path.join(ROOT_DIR, ".github", "agents", "README.template.md")

def strip_oss2():
    """Removes the unused oss2 dependency from requirements.txt."""
    if not os.path.exists(REQUIREMENTS_FILE):
        return
    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(REQUIREMENTS_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip() != "oss2":
                f.write(line)
    print("Stripped 'oss2' from requirements.txt")

def translate_frontend():
    """Translates UI using exact string and Unicode matching, sorted by length to prevent substring corruption."""
    translation_map = {
        "layouts/AdminLayout.tsx": {
            '"运行状态"': '"Status"',
            '"账号管理"': '"Accounts"',
            '"接口测试"': '"API Test"',
            '"图片生成"': '"Image Gen"',
            '"系统设置"': '"Settings"',
        },
        "pages/Dashboard.tsx": {
            "运行状态": "Runtime Status",
            "状态获取失败，请在「系统设置」检查您的当前会话 Key。": "Failed to fetch status. Check your Session Key in Settings.",
            "全局并发监控与千问账号池概览（每 3 秒自动刷新）。": "Global concurrency monitor & account pool overview (auto-refresh every 3s).",
            "可用账号": "Available Accounts",
            "当前并发": "Active Requests",
            "排队请求": "Queued Requests",
            "限流号/失效号": "Rate-limited / Invalid",
            "Chat_ID 预热池": "Chat ID Warmup Pool",
            "异步任务": "Async Tasks",
            "账号并发详情": "Account Concurrency Detail",
            "邮箱": "Email",
            "状态": "Status",
            "在途": "In-flight",
            "预热 chat_id": "Warmed chat_id",
            "连失": "Consec. Failures",
            "限流次": "Rate-limit Hits",
            "API 接口池": "API Endpoint Pool",
            "健康检查": "Health Check",
            "未启用": "Disabled",
            "兼容主流 AI 协议的调用入口，默认无需认证，或通过 API Key 访问。": "Entry points compatible with major AI protocols. No auth required by default, or use an API Key.",
            "`共 ${acc.total ?? 0} 个`": "`total: ${acc.total ?? 0}`",
            "`全局上限 ${acc.global_in_use ?? 0}`": "`global cap: ${acc.global_in_use ?? 0}`",
            "`队列上限 ${acc.max_queue_size ?? 0}`": "`queue cap: ${acc.max_queue_size ?? 0}`",
            "`每账号目标 ${pool.target_per_account}  · TTL ${Math.round((pool.ttl_seconds || 0) / 60)} 分钟`": "`target per acc ${pool.target_per_account} · TTL ${Math.round((pool.ttl_seconds || 0) / 60)} min`",
        },
        "pages/AccountsPage.tsx": {
            # Standard Literals
            "账号管理": "Account Management",
            "管理通义千问上游账号池。": "Manage the upstream Qwen account pool.",
            "刷新状态": "Refresh",
            "一键自动化获取新号": "Auto-Register New Account",
            "手动添加账号": "Add Account Manually",
            "邮箱 (选填)": "Email (optional)",
            "可留空 (或输入密语解锁)": "Leave blank",
            "密码 (选填)": "Password (optional)",
            "用于自愈 / 或密语": "For auto-recovery",
            "Token (必填)": "Token (required)",
            "获取 Token 方法：打开": "How to get a Token: Open",
            "登录后，": "after logging in,",
            "复制其值粘贴到下方。": "Copy the value and paste it below.",
            "暂无账号数据": "No accounts found",
            
            # Critical Unicode Escapes & Template Literals
            r"\u9a8c\u8bc1\u5931\u8d25\uff1a${statusText(data) || localizeError(data.error)}": "Verification failed: ${statusText(data) || localizeError(data.error)}",
            r"\u6fc0\u6d3b\u5931\u8d25\uff1a${localizeError(data.error || data.message)}": "Activation failed: ${localizeError(data.error || data.message)}",
            r"\u6fc0\u6d3b\u8bf7\u6c42\u5931\u8d25": "Activation request failed",
            r"\u5220\u9664\u8d26\u53f7": "Delete account",
            r"Token \u65e0\u6548\u6216\u8ba4\u8bc1\u5931\u8d25": "Token invalid or auth failed",
            r"\u9a8c\u8bc1\u8bf7\u6c42\u5931\u8d25": "Verification request failed",
            r"\u5168\u91cf\u5de1\u68c0\u8bf7\u6c42\u5931\u8d25": "Verify-all request failed",
            r"\u5355\u72ec\u9a8c\u8bc1": "Verify",
            r"\u5176\u4ed6\u5931\u6548": "Other Invalid",
            r"\u53ef\u7528": "Available",
            r"\u672a\u6fc0\u6d3b": "Inactive",
            r"\u9650\u6d41": "Rate Limited",
            r"\u5c01\u7981": "Banned",
            r"\u8ba4\u8bc1\u5931\u6548": "Auth Failed",
            r"\u5931\u6548": "Invalid",
            r"\u672a\u77e5\u9519\u8bef": "Unknown Error",
            r"\u8d26\u53f7\u7ba1\u7406": "Account Management",
            r"\u5168\u91cf\u5de1\u68c0": "Verify All",
            r"\u5237\u65b0\u72b6\u6001": "Refresh Status",
            r"\u4e00\u952e\u83b7\u53d6\u65b0\u53f7": "Auto-register",
            r"\u6b63\u5728\u6ce8\u518c...": "Registering...",
            r"\u624b\u52a8\u6ce8\u5165\u8d26\u53f7": "Inject Account Manually",
            r"Token\uff08\u5fc5\u586b\uff09": "Token (required)",
            r"\u90ae\u7bb1\uff08\u9009\u586b\uff09": "Email (optional)",
            r"\u5bc6\u7801\uff08\u9009\u586b\uff09": "Password (optional)",
            r"\u6ce8\u5165\u8d26\u53f7": "Inject Account",
            r"\u8d26\u53f7\u5217\u8868": "Account List",
            r"\u8d26\u53f7": "Account",
            r"\u72b6\u6001": "Status",
            r"\u5e76\u53d1\u8d1f\u8f7d": "Concurrency",
            r"\u8bf4\u660e": "Description",
            r"\u64cd\u4f5c": "Actions",
            r"\u6fc0\u6d3b": "Activate",
            r"\u7ebf\u7a0d": "threads",
            r"\u6b63\u5728\u6fc0\u6d3b ${targetEmail}...": "Activating ${targetEmail}...",
            r"\u8d26\u53f7\u6b63\u5728\u6fc0\u6d3b\u4e2d\uff0c\u8bf7\u7a0d\u540e\u5237\u65b0\uff1a${targetEmail}": "Activating, retry later: ${targetEmail}",
            r"\u6fc0\u6d3b\u6210\u529f\uff1a${targetEmail}": "Activated: ${targetEmail}",
            r"\u6b63\u5728\u5e76\u53d1\u5de1\u68c0\u6240\u6709\u8d26\u53f7...": "Verifying all accounts...",
            r"\u5168\u91cf\u5de1\u68c0\u5b8c\u6210\uff0c\u5e76\u53d1\u6570\uff1a${data.concurrency || 1}": "Verify complete, concurrency: ${data.concurrency || 1}",
            r"\u5168\u91cf\u5de1\u68c0\u5931\u8d25": "Verify all failed",
            r"\u9884\u8ba1 ${seconds} \u79d2\u540e\u6062\u590d": "Est. recovery in ${seconds}s",
            r"\u8d26\u53f7\u6b63\u5728\u6fc0\u6d3b\u4e2d\uff0c\u8bf7\u7a0d\u540e\u5237\u65b0": "Activating, retry later",
            r"\u6fc0\u6d3b\u94fe\u63a5\u6216 Token \u83b7\u53d6\u5931\u8d25": "Activation link/token failed",
            r"\u5237\u65b0\u8d26\u53f7\u5217\u8868\u5931\u8d25\uff0c\u8bf7\u68c0\u67e5\u4f1a\u8bdd\u5bc6\u94a5": "Refresh failed, check session key",
            r"\u6b63\u5728\u6ce8\u5165\u8d26\u53f7...": "Injecting account...",
            r"\u8d26\u53f7\u5df2\u52a0\u5165\u8d26\u53f7\u6c60": "Account added to pool",
            r"\u8d26\u53f7\u6ce8\u5165\u5931\u8d25": "Account injection failed",
            r"\u6b63\u5728\u5220\u9664 ${targetEmail}...": "Deleting ${targetEmail}...",
            r"\u5df2\u5220\u9664 ${targetEmail}": "Deleted ${targetEmail}",
            r"\u5220\u9664\u8d26\u53f7\u5931\u8d25": "Delete account failed",
            r"\u6b63\u5728\u81ea\u52a8\u6ce8\u518c\u65b0\u8d26\u53f7\uff0c\u8bf7\u7a0d\u5019...": "Auto-registering...",
            r"\u8d26\u53f7\u5df2\u6ce8\u518c\uff0c\u4f46\u4ecd\u9700\u6fc0\u6d3b\uff1a${data.email}": "Registered, needs activation: ${data.email}",
            r"\u6ce8\u518c\u6210\u529f\uff1a${data.email}": "Registration success: ${data.email}",
            r"\u81ea\u52a8\u6ce8\u518c\u5931\u8d25": "Auto-registration failed",
            r"\u6b63\u5728\u9a8c\u8bc1 ${targetEmail}...": "Verifying ${targetEmail}...",
            r"\u9a8c\u8bc1\u901a\u8fc7\uff1a${targetEmail}": "Verified: ${targetEmail}",
            r"\u6682\u65e0\u8d26\u53f7\uff0c\u8bf7\u624b\u52a8\u6ce8\u5165\u6216\u4e00\u952e\u83b7\u53d6\u65b0\u53f7\u3002": "No accounts, please inject manually or auto-register.",
            r"\u7edf\u4e00\u7ba1\u7406\u4e0a\u6e38\u8d26\u53f7\u6c60\uff0c\u5e76\u533a\u5206\u672a\u6fc0\u6d3b\u3001\u9650\u6d41\u3001\u5c01\u7981\u4e0e\u5931\u6548\u72b6\u6001\u3002": "Manage upstream account pool and track statuses.",
            r"\u8bf7\u5148\u5728 chat.qwen.ai \u767b\u5f55\uff0c\u7136\u540e\u6309 F12 \u6253\u5f00\u5f00\u53d1\u8005\u5de5\u5177\uff0c\u5728 Application / Storage \u91cc\u7684 Local Storage / \u672c\u5730\u5b58\u50a8 \u4e2d\u627e\u5230 token \u5e76\u76f4\u63a5\u590d\u5236\u5b8c\u6574\u539f\u59cb\u503c\u7c98\u8d34\u5230\u4e0b\u65b9\u8f93\u5165\u6846\u3002": "Log into chat.qwen.ai, open F12 DevTools -> Application -> Local Storage, copy the token and paste it below.",
            r"\u91cd\u8981\uff1a\u8bf7\u53ea\u7c98\u8d34 Local Storage / \u672c\u5730\u5b58\u50a8 \u91cc\u7684 token \u539f\u59cb\u503c\uff0c\u4e0d\u8981\u4ece Network \u8bf7\u6c42\u6216 Authorization \u8bf7\u6c42\u5934\u4e2d\u63d0\u53d6\u3002": "Important: Only paste the raw token from Local Storage. Do not extract from Network or Authorization headers.",
            r"\u8bf7\u4e0d\u8981\u5e26 Bearer \u524d\u7f00\uff0c\u4e5f\u4e0d\u8981\u7c98\u8d34\u6574\u6bb5 Authorization \u6587\u672c\u3002\u90ae\u7bb1\u548c\u5bc6\u7801\u53ef\u4ee5\u4e0d\u586b\uff0c\u7cfb\u7edf\u4f1a\u5728\u6ce8\u5165\u524d\u5148\u9a8c\u8bc1 token \u662f\u5426\u6709\u6548\u3002": "Do not include the Bearer prefix. Email/Password are optional, token will be verified before injection.",
            r"\u7c98\u8d34\u4ece Local Storage / \u672c\u5730\u5b58\u50a8 \u76f4\u63a5\u590d\u5236\u7684 token": "Paste token from Local Storage",
            r"\u90ae\u7bb1\u5730\u5740": "Email address",
            r"\u7528\u4e8e\u81ea\u52a8\u5237\u65b0\u6216\u6fc0\u6d3b": "For auto-refresh/activation",
            r"\u8bf7\u5148\u586b\u5199 Token": "Please enter Token",
            r"\u8d26\u53f7\u5217\u8868\u5df2\u5237\u65b0": "Account list refreshed",
            r"\u8d26\u53f7\u6ce8\u5165\u8bf7\u6c42\u5931\u8d25": "Account injection request failed",
            r"\u81ea\u52a8\u6ce8\u518c\u8bf7\u6c42\u5931\u8d25": "Auto-registration request failed",
        },
        "pages/SettingsPage.tsx": {
            "配置获取失败，请检查会话 Key": "Failed to fetch config, check your session key",
            "请输入 Key": "Please enter a key",
            "Key 已保存到本地，刷新数据...": "Key saved locally, refreshing...",
            "Key 已清除": "Key cleared",
            "并发配置已保存（运行时立即生效）": "Concurrency config saved (effective immediately)",
            "预热池配置已保存（下一轮刷新生效）": "Warmup pool config saved (effective next refresh)",
            "保存失败": "Save failed",
            "模型映射规则已更新": "Model alias rules updated",
            "JSON 格式错误，请检查语法": "Invalid JSON format, check syntax",
            "系统设置": "System Settings",
            "管理控制台认证与网关运行时配置。": "Manage console auth and gateway runtime config.",
            "刷新配置": "Refresh Config",
            "配置已刷新": "Config refreshed",
            "当前会话 Key": "Session Key",
            "将已有的 API Key 粘贴到此处，控制台将使用它进行所有的管理操作。（保存在浏览器本地）": "Paste your API Key here. The console will use it for all admin operations. (Stored in browser local storage)",
            "sk-qwen-... 或默认管理员密钥 admin": "sk-qwen-... or default admin key",
            "保存并发设置": "Save Concurrency",
            "保存预热池设置": "Save Pool Settings",
            "保存映射": "Save Aliases",
            "保存": "Save",
            "清除": "Clear",
            "连接信息": "Connection Info",
            "API 基础地址 (Base URL)": "API Base URL",
            "核心并发参数": "Concurrency Settings",
            "运行时并发槽位与排队阈值（需要在后端 config.json 中修改后重启生效）。": "Runtime concurrency slots and queue threshold (requires restart after modifying backend config.json).",
            "当前系统版本": "System Version",
            "单账号最大并发 (max_inflight_per_account)": "Max Concurrency per Account (max_inflight_per_account)",
            "每个上游账号同时处理的请求数。太大易被封，太小不充分利用。": "Concurrent requests per upstream account. Too high risks bans, too low wastes resources.",
            "全局并发上限 (global_max_inflight)": "Global Max Concurrency (global_max_inflight)",
            "所有账号合计同时在途请求的硬上限。0 = 不限。对应 Dashboard 的\"异步任务\"峰值。": "Hard limit for total in-flight requests. 0 = unlimited. Corresponds to 'Async Tasks' in Dashboard.",
            "预建 chat_id 规避上游 /chats/new 握手 (0.5~6s)。运行时修改立即生效。": "Pre-create chat_ids to skip /chats/new handshake (0.5~6s). Effective immediately.",
            "每账号目标数 (target)": "Target per account (target)",
            "每个账号预先挂多少个 chat_id 等着。默认 5。": "Number of chat_ids to pre-warm per account. Default 5.",
            "TTL (分钟)": "TTL (minutes)",
            "chat_id 超过此时长则丢弃重建，避免被上游静默回收。默认 10。": "Discard and recreate chat_ids after this duration. Default 10.",
            "自动模型映射规则 (Model Aliases)": "Model Alias Rules",
            "下游传入的模型名称将被网关自动路由至以下千问实际模型。请使用标准 JSON 格式编辑。": "Downstream model names are automatically routed to the corresponding Qwen models. Edit in standard JSON format.",
            "使用示例": "Usage Examples",
            "# 流式对话": "# Streaming chat",
            "# Anthropic 格式": "# Anthropic format",
            "# Gemini 格式": "# Gemini format",
        },
        "pages/TokensPage.tsx": {
            "刷新失败，请检查会话 Key": "Refresh failed, check your session key",
            "已生成新的 API Key": "New API Key generated",
            "生成失败，请检查权限": "Generation failed, check permissions",
            "API Key 已删除": "API Key deleted",
            "API Key 分发": "API Key Management",
            "管理可以访问此网关的下游凭证。": "Manage downstream credentials that can access this gateway.",
            "已刷新": "Refreshed",
            "刷新": "Refresh",
            "生成新 Key": "Generate Key",
            "序号": "No.",
            "操作": "Actions",
            "暂无 API Key": "No API Keys found",
        },
        "pages/TestPage.tsx": {
            "网络错误": "Network error",
            "接口测试": "API Test",
            "在此测试您的 API 分发是否正常工作。": "Test whether your API distribution is working correctly.",
            "模型:": "Model:",
            "流式传输 (Stream)": "Stream",
            "清空对话": "Clear Chat",
            "发送一条消息以开始测试，系统将通过 /v1/chat/completions 进行调用。": "Send a message to start testing. The system will call /v1/chat/completions.",
            "思考中...": "Thinking...",
            "输入测试消息...": "Type a test message...",
            "❌ 未知响应: ": "❌ Unknown response: ",
            "❌ 响应为空（账号可能未激活或无可用账号）": "❌ Empty response (account may be inactive or unavailable)",
            "💭 思考过程 ({msg.reasoning.length} 字)": "💭 Thinking process ({msg.reasoning.length} chars)",
        },
        "pages/ImagePage.tsx": {
            "图片生成": "Image Generation",
            "通过 Qwen3.6-Plus 生成 AI 图片，支持多种比例。": "Generate AI images via Qwen3.6-Plus. Multiple aspect ratios supported.",
            "图片描述 (Prompt)": "Image Prompt",
            "图片比例": "Aspect Ratio",
            "生成数量": "Count",
            "{v} 张": "{v}",  
            "生成中...": "Generating...",
            "生成图片": "Generate",
            "正在生成图片...": "Generating image...",
            "图片生成通常需要 10-30 秒，请耐心等待": "Image generation typically takes 10–30 seconds.",
            "生成结果 ({images.length} 张)": "Results ({images.length})",
            "清空": "Clear",
            "图片加载失败": "Image failed to load",
            "下载": "Download",
            "在新窗口打开": "Open in new tab",
            "还没有生成图片": "No images yet",
            "在上方输入描述，点击「生成图片」开始创作": "Enter a prompt above and click Generate.",
            "生成失败: ": "Generation failed: ",  
            "未返回图片，请重试": "No images returned, please retry",  
            "`成功生成 ${newImages.length} 张图片`": "`Generated ${newImages.length} images`",  
            "网络错误": "Network error",  
            "描述你想生成的图片，例如：赛博朋克风格的猫咪，霓虹灯背景，超写实风格": "Describe the image, e.g.: cyberpunk cat, neon background, ultra-realistic",  
            "Ctrl+Enter 快速生成": "Ctrl+Enter to generate",
        }
    }

    for relative_path, replacements in translation_map.items():
        file_path = os.path.join(FRONTEND_SRC_DIR, relative_path)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Sort keys by length descending to mathematically prevent substring corruption
        sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
        
        for cn_str in sorted_keys:
            en_str = replacements[cn_str]
            content = content.replace(cn_str, en_str)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Frontend UI translated to English.")

def rewrite_readme():
    """Deterministically overwrites the README with the Coolify template."""
    if not os.path.exists(TEMPLATE_README):
        print("Template README not found, skipping rewrite.")
        return
    shutil.copyfile(TEMPLATE_README, README_FILE)
    print("README.md deterministically rewritten for Coolify ops.")

if __name__ == "__main__":
    print("Starting automated fork maintenance...")
    strip_oss2()
    translate_frontend()
    rewrite_readme()
    print("Maintenance complete.")
