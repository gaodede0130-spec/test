#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《偶像之路：CXK 传奇》Web 版本
使用 Streamlit 构建
"""

import streamlit as st
import json
import random
from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class PlayerStats:
    """玩家属性"""
    talent: int = 50
    popularity: int = 30
    controversy: int = 0
    loyalty: int = 50
    capital: int = 50

def init_session_state():
    """初始化 session state"""
    if 'player' not in st.session_state:
        st.session_state.player = PlayerStats()
    if 'current_node' not in st.session_state:
        st.session_state.current_node = "start"
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

def show_stats():
    """显示属性面板"""
    p = st.session_state.player
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎤 才艺", f"{p.talent}/100")
        st.progress(p.talent / 100)
        
        st.metric("⚡ 争议", f"{p.controversy}/100")
        st.progress(p.controversy / 100)
    
    with col2:
        st.metric("🔥 人气", f"{p.popularity}/100")
        st.progress(p.popularity / 100)
        
        st.metric("💎 粉丝忠诚度", f"{p.loyalty}/100")
        st.progress(p.loyalty / 100)
    
    with col3:
        st.metric("💰 资本支持", f"{p.capital}/100")
        st.progress(p.capital / 100)

def apply_effects(effects: Dict):
    """应用效果"""
    p = st.session_state.player
    
    for key, value in effects.items():
        if hasattr(p, key):
            current = getattr(p, key)
            new_value = max(0, min(100, current + value))
            setattr(p, key, new_value)

def get_story_nodes():
    """获取故事节点"""
    return {
        "start": {
            "title": "序章：梦想开始的地方",
            "year": "2012年",
            "content": """
**2012年，浙江温州**

你叫蔡小坤，今年14岁，从小就喜欢唱歌跳舞。

最近你看到了湖南卫视《向上吧！少年》的招募信息，这是一个选拔青少年才艺的选秀节目。

你鼓起勇气报名参加了海选...

海选现场，你发挥出色，评委对你的舞蹈印象深刻。
但在200强晋级赛中，你因为紧张忘词，最终止步全国200强。

这次失败让你深受打击。
            """,
            "choices": [
                {
                    "text": "🔥 坚持梦想，继续参加其他选秀",
                    "effect": {"talent": 5, "popularity": 5},
                    "next": "node2_training"
                },
                {
                    "text": "📚 暂时放弃，回学校读书",
                    "effect": {"talent": -5, "popularity": -10},
                    "next": "ending_normal"
                },
                {
                    "text": "✈️ 去韩国当练习生",
                    "effect": {"talent": 10, "capital": -10},
                    "next": "node2_korea"
                }
            ]
        },
        
        "node2_training": {
            "title": "第二章：磨砺",
            "year": "2014年",
            "content": """
**2014年，16岁**

你没有放弃梦想。两年来，你每天坚持练习8小时，唱歌、跳舞、创作，一样都不落下。

机会来了！《星动亚洲》正在招募练习生，这是一个中韩合作的大型偶像养成节目，优秀选手可以去韩国接受专业训练。

你顺利通过选拔，站在了签约的十字路口...
            """,
            "choices": [
                {
                    "text": "📝 签约大公司，去韩国训练",
                    "effect": {"talent": 15, "capital": 20, "controversy": 5},
                    "next": "node3_contract"
                },
                {
                    "text": "🚫 拒绝签约，保持自由身",
                    "effect": {"talent": 5, "capital": -20},
                    "next": "ending_independent"
                },
                {
                    "text": "🏠 选择国内小型公司",
                    "effect": {"talent": 8, "capital": -5},
                    "next": "node3_domestic"
                }
            ]
        },
        
        "node2_korea": {
            "title": "第二章：异国他乡",
            "year": "2014年",
            "content": """
**2014年，16岁**

你独自一人来到韩国，进入了一家小型经纪公司当练习生。

每天的训练强度超乎想象：
- 早上6点起床跑步
- 每天练习12小时以上
- 严格的体重管理
- 韩语学习

同期练习生都很优秀，竞争异常激烈...
            """,
            "choices": [
                {
                    "text": "💪 坚持训练，等待机会",
                    "effect": {"talent": 20, "loyalty": 10},
                    "next": "node3_korea_wait"
                },
                {
                    "text": "🇨🇳 回国参加《星动亚洲》",
                    "effect": {"talent": 10, "popularity": 15},
                    "next": "node3_contract"
                }
            ]
        },
        
        "node3_contract": {
            "title": "第三章：合约风波",
            "year": "2016年",
            "content": """
**2016年，18岁**

经过两年的韩国训练，你的实力突飞猛进。

但回到国内后，你与原公司的理念产生严重分歧：
- 公司想让你走"小鲜肉"流量路线
- 你希望能做自己喜欢的音乐
- 合约条款极为苛刻（长达10年，分成比例极低）

你面临人生重大抉择...
            """,
            "choices": [
                {
                    "text": "⚖️ 打官司解约，哪怕背负巨额债务",
                    "effect": {"capital": -30, "controversy": 20, "loyalty": 20},
                    "next": "node4_idolproducer"
                },
                {
                    "text": "😔 忍辱负重，等合约到期",
                    "effect": {"talent": -10, "capital": 10, "controversy": 5},
                    "next": "ending_wait_contract"
                },
                {
                    "text": "🤝 私下和解，付出代价换自由",
                    "effect": {"capital": -20, "controversy": 10},
                    "next": "node4_idolproducer"
                }
            ]
        },
        
        "node4_idolproducer": {
            "title": "第四章：偶像练习生",
            "year": "2018年",
            "content": """
**2018年，20岁**

终于获得自由身的你，参加了现象级选秀《偶像练习生》。

100位练习生，只有9个出道位。

初舞台，你凭借原创作品《I Wanna Get Love》惊艳全场，获得全场最高评级A，并成为首A选手。

节目播出后，你的人气一路飙升，微博粉丝从几千暴涨到几百万。

但争议也随之而来：有人质疑你的实力...

**出道之夜即将来临，你选择...**
            """,
            "choices": [
                {
                    "text": "🔥 全力以赴，拼C位出道",
                    "effect": {"talent": 10, "popularity": 30, "loyalty": 20},
                    "next": "node5_debut"
                },
                {
                    "text": "😌 保守策略，确保出道位即可",
                    "effect": {"popularity": 15, "loyalty": 10},
                    "next": "node5_safe_debut"
                },
                {
                    "text": "💥 制造话题，走黑红路线",
                    "effect": {"popularity": 40, "controversy": 30, "loyalty": -10},
                    "next": "node5_controversial_debut"
                }
            ]
        },
        
        "node5_debut": {
            "title": "第五章：巅峰出道",
            "year": "2018年4月",
            "content": """
**2018年4月6日**

《偶像练习生》总决赛，你以4700万+票的成绩，**断层第一C位出道**！

与其他8名成员组成NINE PERCENT，你成为这个顶级男团的绝对中心。

出道即巅峰：
- 微博热搜霸榜
- 商业代言接到手软
- 粉丝战斗力爆表
- 成为现象级流量
            """,
            "choices": [
                {
                    "text": "继续故事 ➡️",
                    "effect": {},
                    "next": "node6_nba"
                }
            ]
        },
        
        "node6_nba": {
            "title": "第六章：篮球风波",
            "year": "2019年",
            "content": """
**2019年，21岁**

你成为了NBA新春贺岁大使。

在宣传视频中，你秀了一段篮球+舞蹈的组合技。

没想到，这段视频被恶搞、鬼畜，一夜之间全网都是"鸡你太美"、"你打球像CXK"。

你的形象被严重丑化...

**面对这场舆论风暴，你选择...**
            """,
            "choices": [
                {
                    "text": "📄 发律师函，强硬反击",
                    "effect": {"controversy": 40, "popularity": 20, "loyalty": -10},
                    "next": "node7_solo"
                },
                {
                    "text": "😂 自嘲化解，以柔克刚",
                    "effect": {"controversy": 10, "popularity": 15, "loyalty": 15},
                    "next": "node7_solo"
                },
                {
                    "text": "🤐 冷处理，等待热度过去",
                    "effect": {"controversy": 20, "popularity": -10},
                    "next": "node7_solo"
                }
            ]
        },
        
        "node7_solo": {
            "title": "第七章：单飞之路",
            "year": "2019年10月",
            "content": """
**2019年10月，NINE PERCENT解散。**

团体活动结束，你正式开启个人发展。

站在事业的十字路口，你需要决定未来的方向...
            """,
            "choices": [
                {
                    "text": "🎵 专注音乐，减少综艺曝光",
                    "effect": {"talent": 20, "popularity": -10, "loyalty": 15},
                    "next": "node8_final"
                },
                {
                    "text": "🎬 多栖发展，影视综艺全开",
                    "effect": {"popularity": 20, "talent": -5, "controversy": 10},
                    "next": "node8_final"
                },
                {
                    "text": "💥 专注流量，维持热度至上",
                    "effect": {"popularity": 30, "controversy": 20, "talent": -10},
                    "next": "node8_final"
                }
            ]
        },
        
        "node8_final": {
            "title": "第八章：命运抉择",
            "year": "2023年",
            "content": """
**2023年，25岁**

事业正当红，突然有媒体爆料称你涉及负面新闻。

一时间舆论哗然，代言纷纷解约...

这是职业生涯最大的危机。

**你的选择将决定最终结局...**
            """,
            "choices": [
                {
                    "text": "🚫 立即否认，强硬对抗",
                    "effect": {"controversy": 50, "popularity": -30},
                    "next": "final_ending"
                },
                {
                    "text": "🤐 沉默应对，让时间冲淡",
                    "effect": {"controversy": 30, "popularity": -20},
                    "next": "final_ending"
                },
                {
                    "text": "🙏 真诚道歉，承担责任",
                    "effect": {"controversy": 10, "popularity": -20, "loyalty": 10},
                    "next": "final_ending"
                }
            ]
        },
        
        # 结局
        "ending_normal": {
            "title": "📘 结局：平淡人生",
            "year": "终章",
            "content": """
你的偶像之路平平无奇。

没有大红大紫，也没有彻底失败，就像大多数参加过选秀的年轻人一样，最终被时代遗忘。

但至少，你追逐过梦想。
            """,
            "is_ending": True,
            "ending_type": "normal"
        },
        
        "ending_independent": {
            "title": "🎸 结局：独立音乐人",
            "year": "终章",
            "content": """
你选择保持自由，但也失去了资本的支持。

在小酒吧驻唱，在网络上发布作品，你坚持着纯粹的音乐梦想。

虽然成不了大明星，但你是自己的老板。
            """,
            "is_ending": True,
            "ending_type": "independent"
        },
        
        "ending_wait_contract": {
            "title": "⏳ 结局：十年等待",
            "year": "终章",
            "content": """
你选择了等待合约到期。

十年后，你终于自由了，但最好的青春已经逝去。

市场早已变了模样，你错过了最好的时机...
            """,
            "is_ending": True,
            "ending_type": "wait"
        },
        
        "node3_domestic": {
            "title": "第三章：国内发展",
            "year": "2016年",
            "content": """
你选择了国内的小型公司。

资源有限，但相对自由。你参加了一些小型演出，积累了一些粉丝。

2018年，你看到了《偶像练习生》的机会...
            """,
            "choices": [
                {
                    "text": "参加《偶像练习生》",
                    "effect": {"popularity": 10},
                    "next": "node4_idolproducer"
                }
            ]
        },
        
        "node3_korea_wait": {
            "title": "第三章：韩国岁月",
            "year": "2015-2016",
            "content": """
在韩国的练习生生活持续了两年。

你学到了很多，但出道机会迟迟不来。公司告诉你还需要等待...

2016年，你决定回国发展。
            """,
            "choices": [
                {
                    "text": "回国",
                    "effect": {"talent": 5},
                    "next": "node3_contract"
                }
            ]
        },
        
        "node5_safe_debut": {
            "title": "第五章：稳妥出道",
            "year": "2018年",
            "content": """
你选择了保守策略，最终排名第5顺利出道。

虽然没有C位那么耀眼，但你避免了过多的争议，稳扎稳打地开始了自己的偶像之路...
            """,
            "choices": [
                {
                    "text": "继续",
                    "effect": {},
                    "next": "node6_nba"
                }
            ]
        },
        
        "node5_controversial_debut": {
            "title": "第五章：黑红出道",
            "year": "2018年",
            "content": """
靠着制造话题，你成功C位出道，但也积累了大量黑粉。

从出道第一天起，你就处于舆论的风口浪尖...
            """,
            "choices": [
                {
                    "text": "继续",
                    "effect": {},
                    "next": "node6_nba"
                }
            ]
        },
        
        "final_ending": {
            "title": "终章：最终结局",
            "year": "2024年",
            "content": "",
            "is_ending": True,
            "ending_type": "dynamic"
        }
    }

def determine_ending():
    """确定结局"""
    p = st.session_state.player
    
    if p.controversy >= 90:
        return {
            "title": "🚫 E级结局：被封杀退圈",
            "content": """
负面事件爆发，舆论不可挽回。

代言全部解约，作品被下架，社交账号被封...

你不得不退出娱乐圈，曾经的一切仿佛一场梦。

💔 成也流量，败也流量。
            """,
            "grade": "E"
        }
    elif p.controversy >= 70:
        return {
            "title": "⚡ C级结局：争议明星",
            "content": """
黑红也是红。

你身上永远不缺争议和话题，喜欢的人很喜欢，讨厌的人很讨厌。

商业价值依然很高，但路人缘一般...

💥 争议是你最好的流量密码。
            """,
            "grade": "C"
        }
    elif p.popularity >= 90 and p.capital >= 80:
        return {
            "title": "⭐ A级结局：顶流偶像",
            "content": """
你是现象级顶流，商业价值极高！

代言接到手软，杂志封面常客，粉丝号召力惊人。

虽然争议不断，但你依然是这个时代最具代表性的偶像之一。

🔥 你是真正的流量之王！
            """,
            "grade": "A"
        }
    elif p.talent >= 90 and p.popularity >= 95 and p.controversy < 30:
        return {
            "title": "🏆 S级结局：传奇巨星",
            "content": """
你成为了华语乐坛的标志性人物！

代表作成为经典，你亲自创作的作品获得业内广泛认可，
从偶像成功转型为真正的音乐人。

你的演唱会场场爆满，成为一代人的青春记忆。

🎉 恭喜达成完美结局！
            """,
            "grade": "S"
        }
    elif p.talent >= 85 and p.controversy < 40:
        return {
            "title": "🎵 B级结局：实力派歌手",
            "content": """
你选择了用作品说话。

虽然流量不是最高，但圈内口碑极佳，音乐作品质量上乘。

你有一群死忠歌迷，他们爱你的音乐，而不是你的数据。

🎤 音乐人，用作品征服听众！
            """,
            "grade": "B"
        }
    elif p.popularity >= 80 and p.loyalty < 30:
        return {
            "title": "🌅 D级结局：昙花一现",
            "content": """
曾经红极一时，如今归于平淡。

选秀带来的热度没有持续，没有核心作品支撑，粉丝逐渐流失。

现在的你偶尔参加商演...

📉 娱乐圈，就是这么残酷。
            """,
            "grade": "D"
        }
    elif p.capital < 30 and p.talent >= 70:
        return {
            "title": "🎬 F级结局：转型幕后",
            "content": """
聚光灯不再，但你没有离开音乐。

你转型成为音乐制作人，为新人写歌、制作专辑。

虽然不再站在台前，但你的作品通过别人继续发光。

🎹 幕后英雄，另一种精彩。
            """,
            "grade": "F"
        }
    else:
        return {
            "title": "📘 普通结局：平淡人生",
            "content": """
你的偶像之路平平无奇。

没有大红大紫，也没有彻底失败...

但至少，你追逐过梦想。

🌊 人海浮沉，各自安好。
            """,
            "grade": "N"
        }

def show_ending():
    """显示结局"""
    ending = determine_ending()
    
    st.balloons()
    
    st.markdown(f"# {ending['title']}")
    st.markdown(ending['content'])
    
    # 结局等级徽章
    grade_colors = {
        "S": "🥇",
        "A": "🥈", 
        "B": "🥉",
        "C": "📜",
        "D": "📄",
        "E": "💔",
        "F": "🎭",
        "N": "📘"
    }
    
    st.markdown(f"### 结局等级: {grade_colors.get(ending['grade'], '📄')} {ending['grade']}级")
    
    st.markdown("---")
    st.markdown("### 📊 最终属性")
    show_stats()
    
    st.markdown("---")
    if st.button("🔄 重新开始", key="restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    """主函数"""
    st.set_page_config(
        page_title="偶像之路：CXK 传奇",
        page_icon="🌟",
        layout="wide"
    )
    
    init_session_state()
    
    # 标题
    st.markdown("""
    <div style="text-align: center;">
        <h1>🌟 偶像之路：CXK 传奇 🌟</h1>
        <p><em>一款基于真实出道历程的文字冒险游戏</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # 获取当前节点
    nodes = get_story_nodes()
    current = nodes.get(st.session_state.current_node)
    
    if not current:
        st.error("游戏出错：找不到当前节点")
        return
    
    # 显示故事内容
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## 📖 {current['title']}")
        st.markdown(f"*📅 {current['year']}*")
        st.markdown("---")
        st.markdown(current['content'])
        
        # 如果是结局
        if current.get('is_ending'):
            if current.get('ending_type') == 'dynamic':
                show_ending()
            else:
                st.balloons()
                st.markdown("### 🎮 游戏结束")
                if st.button("🔄 重新开始"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
            return
        
        # 显示选择
        st.markdown("---")
        st.markdown("### 💭 你的选择：")
        
        for i, choice in enumerate(current['choices']):
            if st.button(choice['text'], key=f"choice_{i}"):
                # 应用效果
                if choice.get('effect'):
                    apply_effects(choice['effect'])
                
                # 记录历史
                st.session_state.history.append({
                    "node": st.session_state.current_node,
                    "choice": choice['text']
                })
                
                # 进入下一节点
                st.session_state.current_node = choice['next']
                st.rerun()
    
    with col2:
        st.markdown("### 📊 当前状态")
        show_stats()
        
        st.markdown("---")
        st.markdown("### 📝 历史记录")
        for i, h in enumerate(st.session_state.history[-5:], 1):
            st.markdown(f"{i}. {h['choice'][:20]}...")

if __name__ == "__main__":
    main()
