#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import os

# 颜色定义 - 深绿色主题
DARK_GREEN = colors.HexColor('#1B5E20')
MID_GREEN = colors.HexColor('#2E7D32')
LIGHT_GREEN = colors.HexColor('#4CAF50')
VERY_LIGHT_GREEN = colors.HexColor('#E8F5E9')
ACCENT_GREEN = colors.HexColor('#388E3C')
WHITE = colors.white
TEXT_DARK = colors.HexColor('#1A1A1A')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
GRID_GREEN = colors.HexColor('#A5D6A7')

# 页面尺寸 - A4横向
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

OUTPUT_PATH = '/Users/omi/.openclaw/workspace-pet-macos/swot_openclaw_llm.pdf'

class SWOTCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        canvas.Canvas.showPage(self)

    def save(self):
        self._draw_page()
        canvas.Canvas.save(self)

    def _draw_page(self):
        pass  # 使用 Platypus 绘制


def draw_page_background(c, width, height):
    """绘制深绿色主题背景"""
    # 主背景 - 渐变效果用色块模拟
    c.setFillColor(DARK_GREEN)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # 顶部装饰条
    c.setFillColor(MID_GREEN)
    c.rect(0, height - 60, width, 60, fill=1, stroke=0)

    # 底部装饰条
    c.setFillColor(MID_GREEN)
    c.rect(0, 0, width, 30, fill=1, stroke=0)

    # 右侧细装饰线
    c.setStrokeColor(LIGHT_GREEN)
    c.setLineWidth(2)
    c.line(width - 3, 30, width - 3, height - 60)


def draw_header(c, width, height):
    """绘制标题区"""
    # 主标题
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 38, "OpenClaw + LLM 市场调研与趋势分析")

    # 副标题
    c.setFillColor(GRID_GREEN)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 54, "SWOT 战略分析 | AI 赋能企业洞察")


def draw_swot_grid(c, width, height):
    """绘制SWOT四个格子"""
    # 格子尺寸
    margin = 1.8 * cm
    top_offset = 3.8 * cm
    bottom_offset = 1.8 * cm

    available_width = width - 2 * margin
    available_height = height - top_offset - bottom_offset

    cell_w = available_width / 2
    cell_h = available_height / 2
    gap = 0.3 * cm

    # 象限标签颜色
    colors_map = {
        'S': (MID_GREEN, 'S', '优势 Strengths'),
        'W': (ACCENT_GREEN, 'W', '劣势 Weaknesses'),
        'O': (colors.HexColor('#1565C0'), 'O', '机会 Opportunities'),
        'T': (colors.HexColor('#C62828'), 'T', '威胁 Threats'),
    }

    # 象限内容
    swot_data = {
        'S': [
            '✅ 全天候网络检索：实时抓取行业新闻、社交媒体、电商数据',
            '✅ 多源数据整合：网页/社媒/数据库一站式汇聚',
            '✅ 跨会话记忆：持续积累行业知识，构建企业专属洞察库',
            '✅ 多格式输出：PDF报告/图表/摘要，按需生成',
            '✅ 成本效益：相比传统调研团队，效率提升10倍以上',
        ],
        'W': [
            '⚠️ 平台限制：需登录内容（小红书、微信等）抓取受限',
            '⚠️ 商业数据库缺口：无法直接访问尼尔森/欧睿等付费数据',
            '⚠️ 推理深度有限：复杂因果关系和定性判断需人工复核',
            '⚠️ 实时性依赖网络：离线场景无法工作',
        ],
        'O': [
            '🚀 中小企业需求旺：预算有限但渴望数据驱动决策',
            '🚀 国产替代趋势：企业倾向灵活可控的国产AI工具',
            '🚀 垂直行业深耕：宠物/医疗/消费等赛道调研需求爆发',
            '🚀 快速验证市场：新品上市前快速摸清竞争格局',
        ],
        'T': [
            '🔴 数据隐私风险：企业敏感信息需严格隔离',
            '🔴 信任门槛：管理层对AI洞察的接受度需培育',
            '🔴 信息准确性：AI幻觉可能导致误判，需风控机制',
            '🔴 平台封禁风险：高频抓取可能触发反爬机制',
        ],
    }

    positions = {
        'S': (margin, top_offset + cell_h + gap/2, cell_w - gap, cell_h - gap),
        'W': (margin + cell_w, top_offset + cell_h + gap/2, cell_w - gap, cell_h - gap),
        'O': (margin, top_offset, cell_w - gap, cell_h - gap),
        'T': (margin + cell_w, top_offset, cell_w - gap, cell_h - gap),
    }

    for key in ['S', 'W', 'O', 'T']:
        x, y, w, h = positions[key]
        bg_color, label, title = colors_map[key]
        items = swot_data[key]

        # 象限背景
        c.setFillColor(bg_color)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=0)

        # 标题栏背景
        c.setFillColor(colors.HexColor('#FFFFFF') if key in ['O', 'T'] else WHITE)
        c.setFillColor(WHITE)
        title_bar_h = 0.65 * cm
        c.roundRect(x, y + h - title_bar_h - 0.15*cm, w, title_bar_h, 6, fill=1, stroke=0)

        # 象限标签
        c.setFillColor(bg_color)
        c.roundRect(x + 0.15*cm, y + h - title_bar_h - 0.15*cm, 0.65*cm, title_bar_h, 3, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + 0.15*cm + 0.325*cm, y + h - title_bar_h - 0.15*cm + 0.12*cm, label)

        # 标题文字
        c.setFillColor(TEXT_DARK if key in ['O', 'T'] else WHITE)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 0.95*cm, y + h - title_bar_h - 0.15*cm + 0.12*cm, title)

        # 内容区
        c.setFillColor(WHITE)
        line_height = 0.52 * cm
        start_y = y + h - title_bar_h - 0.15*cm - 0.35*cm

        for i, item in enumerate(items):
            item_y = start_y - i * line_height
            if item_y < y + 0.2*cm:
                break
            # 内容文字（截断超长内容）
            display_text = item
            c.setFont("Helvetica", 8.5)
            c.drawString(x + 0.2*cm, item_y, display_text)


def draw_footer(c, width):
    """绘制页脚"""
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 7.5)
    c.drawString(1.8*cm, 0.8*cm, "© OpenClaw + LLM 赋能企业市场调研 | 2026")
    c.drawRightString(width - 1.8*cm, 0.8*cm, "Confidential · 仅供内部分享")


def create_pdf():
    c = canvas.Canvas(OUTPUT_PATH, pagesize=landscape(A4))
    width, height = landscape(A4)

    # 绘制背景
    draw_page_background(c, width, height)

    # 绘制标题
    draw_header(c, width, height)

    # 绘制SWOT网格
    draw_swot_grid(c, width, height)

    # 绘制页脚
    draw_footer(c, width)

    c.save()
    print(f"✅ SWOT PDF 已生成: {OUTPUT_PATH}")


if __name__ == '__main__':
    create_pdf()
