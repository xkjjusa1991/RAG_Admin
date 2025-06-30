'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-26 14:01:52
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-30 17:26:05
FilePath: \RAG_Admin\app\services\mineru_service.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import subprocess
import os
import re
from app.core.config import settings

class MinerUService:
    def __init__(self, image_dir=None, md_dir=None):
        self.image_dir = image_dir or settings.MINERU_IMAGE_DIR
        self.md_dir = md_dir or settings.MINERU_MD_DIR
        self.image_url_prefix = getattr(settings, 'MINERU_IMAGE_URL_PREFIX', None)
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.md_dir, exist_ok=True)

    def parse_pdf(self, pdf_path: str, output_basename: str = None, method: str = "auto", lang: str = None):
        """
        :param pdf_path: 输入文件路径
        :param output_basename: 输出文件基础名
        :param method: 解析方式，auto/txt/ocr
        :param lang: OCR语言，如ch/en等
        :return: markdown文本内容
        """
        if output_basename is None:
            output_basename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = self.md_dir
        cmd = [
            "mineru",
            "-p", pdf_path,
            "-o", output_dir,
            "-m", method,
            "-t", "true"
        ]
        if lang:
            cmd += ["-l", lang]
        print(f"[MinerUService] 调用命令: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[MinerUService] mineru stdout:\n{result.stdout}")
            print(f"[MinerUService] mineru stderr:\n{result.stderr}")
        except Exception as e:
            print(f"[MinerUService] mineru命令行调用失败: {e}")
            print(f"[MinerUService] stdout: {getattr(e, 'stdout', '')}")
            print(f"[MinerUService] stderr: {getattr(e, 'stderr', '')}")
            raise RuntimeError(f"mineru命令行调用失败: {e}\nstdout: {getattr(e, 'stdout', '')}\nstderr: {getattr(e, 'stderr', '')}")

        # 根据method动态拼接输出子目录
        output_subdir = os.path.join(output_dir, output_basename, method)
        md_file = os.path.join(output_subdir, f"{output_basename}.md")
        print(f"[MinerUService] 期望输出文件: {md_file}")
        md_content = open(md_file, encoding="utf-8").read() if os.path.exists(md_file) else ""
        print(f"[MinerUService] md_content长度: {len(md_content)}")

        # 处理图片链接为绝对路径
        url_prefix = self.image_url_prefix
        images_dir = os.path.join(output_subdir, "images")
        if url_prefix:
            def repl(match):
                orig_path = match.group(1)
                if os.path.isabs(orig_path):
                    return match.group(0)
                abs_path = os.path.join(url_prefix, os.path.basename(orig_path)).replace('\\', '/')
                return f'![]({abs_path})'
            md_content = re.sub(r'!\[.*?\]\((.*?)\)', repl, md_content)
        else:
            print("[MinerUService] 未配置图片绝对路径前缀，图片链接保持原样")
        return md_content 