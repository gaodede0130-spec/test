#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《偶像之路：CXK 传奇》
基于蔡徐坤出道历程的文字冒险游戏
"""

import json
import random
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class PlayerStats:
    """玩家属性"""
    talent: int = 50  # 才艺
    popularity: int = 30  # 人气
    controversy: int = 0  # 争议
    loyalty: int = 50  # 粉丝忠诚度
    capital: int = 50  # 资本支持
    
    def show(self):
        """显示属性面板"""
        print("\n" + "="*40)
        print("📊 当前状态")
        print("="*40)
        print(f"🎤 才艺:     {'█' * (self.talent//10)}{'░' * (10-self.talent//10)} {self.talent}")
        print(f"🔥 人气:     {'█' * (self.popularity//10)}{'░' * (10-self.popularity//10)} {self.popularity}")
        print(f"⚡ 争议:     {'█' * (self.controversy//10)}{'░' * (10-self.controversy//10)} {self.controversy}")
        print(f"💎 粉丝忠诚度: {'█' * (self.loyalty//10)}{'░' * (10-self.loyalty//10)} {self.loyalty}")
        print(f"💰 资本支持:  {'█' * (self.capital//10)}{'░' * (10-self.capital//10)} {self.capital}")
        print("="*40)

class StoryNode:
    """故事节点"""
    def __init__(self, id: str, title: str, content: str, choices: List[Dict]):
        self.id = id
        self.title = title
        self.content = content
        self.choices = choices

class CXKGame:
    """游戏主类"""
    
    def __init__(self):
        self.player = PlayerStats()
        self.current_node = "start"
        self.history = []
        self.year = 2012
        self.load_story()
        
    def load_story(self):
        """加载剧情数据"""
        self.story_nodes = {
            "start": StoryNode(
                "start",
                "序章：梦想开始的地方",
                """
    2012年，浙江温州

    你叫蔡小坤，今年14岁，从小就喜欢唱歌跳舞。
    最近你看到了湖南卫视《向上吧！少年》的招募信息，
    这是一个选拔青少年才艺的选秀节目。

    你鼓起勇气报名参加了海选...

    海选现场，你发挥出色，评委对你的舞蹈印象深刻。
    但在200强晋级赛中，你因为紧张忘词，最终止步全国200强。

    这次失败让你深受打击。
                """,
                [
                    {
                        "text": "🔥 坚持梦想，继续参加其他选秀",
                        "effect": {"talent": +5, "popularity": +5, "controversy": 0},
                        "next": "node2_training"
                    },
                    {
                        "text": "📚 暂时放弃，回学校专心读书",
                        "effect": {"talent": -5, "popularity": -10, "controversy": 0},
                        "next": "node2_school"
                    },
                    {
                        "text": "✈️ 去韩国当练习生",
                        "effect": {"talent": +10, "capital": -10, "controversy": 0},
                        "next": "node2_korea"
                    }
                ]
            ),
            
            "node2_training": StoryNode(
                "node2_training",
                "第二章：磨砺",
                """
    2014年，16岁

    你没有放弃梦想。两年来，你每天坚持练习8小时，
    唱歌、跳舞、创作，一样都不落下。

    机会来了！《星动亚洲》正在招募练习生，
    这是一个中韩合作的大型偶像养成节目，
    优秀选手可以去韩国接受专业训练。

    你顺利通过选拔，站在了签约的十字路口。
    面前有三家公司的合约...
                """,
                [
                    {
                        "text": "📝 签约大公司，获得去韩国训练的机会",
                        "effect": {"talent": +15, "capital": +20, "controversy": 5},
                        "next": "node3_contract"
                    },
                    {
                        "text": "🚫 拒绝签约，保持自由身",
                        "effect": {"talent": +5, "capital": -20, "controversy": 0},
                        "next": "node3_independent"
                    },
                    {
                        "text": "🏠 选择国内小型公司",
                        "effect": {"talent": +8, "capital": -5, "controversy": 0},
                        "next": "node3_domestic"
                    }
                ]
            ),
            
            "node2_school": StoryNode(
                "node2_school",
                "第二章：平凡之路",
                """
    2014年，16岁

    你选择了回到学校，暂时放下了明星梦。
    但内心深处，那个舞台梦从未熄灭。

    你在学校的文艺汇演上总是最耀眼的那个，
    同学们都说你应该去当明星。

    两年后，高考在即，但你收到了《星动亚洲》的邀请函...
                """,
                [
                    {
                        "text": "🎤 休学参加节目",
                        "effect": {"talent": +10, "popularity": +10, "controversy": 5},
                        "next": "node3_contract"
                    },
                    {
                        "text": "📖 继续读书，放弃这次机会",
                        "effect": {"talent": -10, "popularity": -20},
                        "next": "ending_normal"
                    }
                ]
            ),
            
            "node2_korea": StoryNode(
                "node2_korea",
                "第二章：异国他乡",
                """
    2014年，16岁

    你独自一人来到韩国，进入了一家小型经纪公司当练习生。
    每天的训练强度超乎想象：
    - 早上6点起床跑步
    - 每天练习12小时以上
    - 严格的体重管理
    - 韩语学习

    同期练习生都很优秀，竞争异常激烈。
    你发现公司资源有限，出道机会渺茫...
                """,
                [
                    {
                        "text": "💪 坚持训练，等待机会",
                        "effect": {"talent": +20, "loyalty": +10},
                        "next": "node3_korea_wait"
                    },
                    {
                        "text": "🇨🇳 回国参加《星动亚洲》",
                        "effect": {"talent": +10, "popularity": +15},
                        "next": "node3_contract"
                    }
                ]
            ),
            
            "node3_contract": StoryNode(
                "node3_contract",
                "第三章：合约风波",
                """
    2016年，18岁

    经过两年的韩国训练，你的实力突飞猛进。
    但回到国内后，你与原公司的理念产生严重分歧：
    - 公司想让你走"小鲜肉"流量路线
    - 你希望能做自己喜欢的音乐
    - 合约条款极为苛刻（长达10年，分成比例极低）

    你面临人生重大抉择...
                """,
                [
                    {
                        "text": "⚖️ 打官司解约，哪怕背负巨额债务",
                        "effect": {"capital": -30, "controversy": +20, "loyalty": +20},
                        "next": "node4_idolproducer"
                    },
                    {
                        "text": "😔 忍辱负重，等合约到期",
                        "effect": {"talent": -10, "capital": +10, "controversy": +5},
                        "next": "node4_wait"
                    },
                    {
                        "text": "🤝 私下和解，付出代价换自由",
                        "effect": {"capital": -20, "controversy": +10},
                        "next": "node4_idolproducer"
                    }
                ]
            ),
            
            "node4_idolproducer": StoryNode(
                "node4_idolproducer",
                "第四章：偶像练习生",
                """
    2018年，20岁

    终于获得自由身的你，参加了现象级选秀《偶像练习生》。
    100位练习生，只有9个出道位。

    初舞台，你凭借原创作品《I Wanna Get Love》惊艳全场，
    获得全场最高评级A，并成为首A选手。

    节目播出后，你的人气一路飙升，
    微博粉丝从几千暴涨到几百万。

    但争议也随之而来：有人质疑你的实力，
    有人说你"油腻"，还有人说你"太娘"。

    出道之夜即将来临，你选择...
                """,
                [
                    {
                        "text": "🔥 全力以赴，拼C位出道",
                        "effect": {"talent": +10, "popularity": +30, "loyalty": +20},
                        "next": "node5_debut"
                    },
                    {
                        "text": "😌 保守策略，确保出道位即可",
                        "effect": {"popularity": +15, "loyalty": +10},
                        "next": "node5_safe_debut"
                    },
                    {
                        "text": "💥 制造话题，走黑红路线",
                        "effect": {"popularity": +40, "controversy": +30, "loyalty": -10},
                        "next": "node5_controversial_debut"
                    }
                ]
            ),
            
            "node5_debut": StoryNode(
                "node5_debut",
                "第五章：巅峰出道",
                """
    2018年4月6日

    《偶像练习生》总决赛，你以4700万+票的成绩，
    断层第一C位出道！

    与其他8名成员组成NINE PERCENT，
    你成为这个顶级男团的绝对中心。

    出道即巅峰：
    - 微博热搜霸榜
    - 商业代言接到手软
    - 粉丝战斗力爆表
    - 成为现象级流量

    但同时，质疑和攻击也从未停止...
                """,
                [
                    {
                        "text": "继续游戏",
                        "effect": {},
                        "next": "node6_nba"
                    }
                ]
            ),
            
            "node6_nba": StoryNode(
                "node6_nba",
                "第六章：篮球风波",
                """
    2019年，21岁

    你成为了NBA新春贺岁大使。
    在宣传视频中，你秀了一段篮球+舞蹈的组合技。

    没想到，这段视频被恶搞、鬼畜，
    一夜之间全网都是"鸡你太美"、"你打球像CXK"。

    你的形象被严重丑化，甚至连一些完全不认识你的人都开始玩梗。

    面对这场舆论风暴，你选择...
                """,
                [
                    {
                        "text": "📄 发律师函，强硬反击",
                        "effect": {"controversy": +40, "popularity": +20, "loyalty": -10},
                        "next": "node7_after_nba"
                    },
                    {
                        "text": "😂 自嘲化解，以柔克刚",
                        "effect": {"controversy": +10, "popularity": +15, "loyalty": +15},
                        "next": "node7_after_nba"
                    },
                    {
                        "text": "🤐 冷处理，等待热度过去",
                        "effect": {"controversy": +20, "popularity": -10},
                        "next": "node7_after_nba"
                    }
                ]
            ),
            
            "node7_after_nba": StoryNode(
                "node7_after_nba",
                "第七章：单飞之路",
                """
    2019年10月，NINE PERCENT解散。

    团体活动结束，你正式开启个人发展。
    站在事业的十字路口，你需要决定未来的方向：

    - 继续做流量偶像，维持曝光
    - 专注音乐创作，提升实力
    - 多栖发展，影视综艺全开
                """,
                [
                    {
                        "text": "🎵 专注音乐，减少综艺曝光",
                        "effect": {"talent": +20, "popularity": -10, "loyalty": +15},
                        "next": "node8_music"
                    },
                    {
                        "text": "🎬 多栖发展，影视综艺全开",
                        "effect": {"popularity": +20, "talent": -5, "controversy": +10},
                        "next": "node8_multi"
                    },
                    {
                        "text": "💥 专注流量，维持热度至上",
                        "effect": {"popularity": +30, "controversy": +20, "talent": -10},
                        "next": "node8_traffic"
                    }
                ]
            ),
            
            "node8_music": StoryNode(
                "node8_music",
                "第八章：创作歌手",
                """
    2020-2021年

    你选择专注音乐创作。
    发行了EP《YOUNG》《迷》，单曲《情人》大火，
    成为各大音乐榜单的常客。

    你亲自参与词曲创作，尝试不同音乐风格，
    从电子到R&B，从抒情到说唱。

    但曝光度下降，热度不如团体时期...
                """,
                [
                    {
                        "text": "继续游戏",
                        "effect": {},
                        "next": "node9_crisis"
                    }
                ]
            ),
            
            "node8_multi": StoryNode(
                "node8_multi",
                "第八章：全能艺人",
                """
    2020-2021年

    你选择了多栖发展：
    - 发行个人单曲
    - 参加多档综艺节目
    - 尝试演戏

    曝光度很高，粉丝基数进一步扩大，
    但"全能"也意味着没有特别突出的领域，
    被质疑"样样通，样样松"...
                """,
                [
                    {
                        "text": "继续游戏",
                        "effect": {},
                        "next": "node9_crisis"
                    }
                ]
            ),
            
            "node8_traffic": StoryNode(
                "node8_traffic",
                "第八章：流量之王",
                """
    2020-2021年

    你选择继续走流量路线，通过各种方式维持热度：
    - 频繁上热搜
    - 粉丝打榜做数据
    - 制造话题和争议

    你确实是顶级流量，商业价值极高，
    但也积累了大量黑粉和负面评价...
                """,
                [
                    {
                        "text": "继续游戏",
                        "effect": {},
                        "next": "node9_crisis"
                    }
                ]
            ),
            
            "node9_crisis": StoryNode(
                "node9_crisis",
                "第九章：至暗时刻",
                """
    2023年，25岁

    事业正当红，突然有媒体爆料称你涉及负面新闻。
    一时间舆论哗然，代言纷纷解约，作品被下架。

    这是职业生涯最大的危机。
    你的选择将决定最终结局...
                """,
                [
                    {
                        "text": "🚫 立即否认，强硬对抗",
                        "effect": {"controversy": +50, "popularity": -30},
                        "next": "ending_check"
                    },
                    {
                        "text": "🤐 沉默应对，让时间冲淡",
                        "effect": {"controversy": +30, "popularity": -20},
                        "next": "ending_check"
                    },
                    {
                        "text": "🙏 真诚道歉，承担责任",
                        "effect": {"controversy": +10, "popularity": -20, "loyalty": +10},
                        "next": "ending_check"
                    }
                ]
            ),
            
            "ending_check": StoryNode(
                "ending_check",
                "终章：结局",
                """
    经过这么多年的起起伏伏，
    你的偶像之路终于走到了终点。

    让我们看看你的最终结局...
                """,
                [
                    {
                        "text": "查看结局",
                        "effect": {},
                        "next": "final_ending"
                    }
                ]
            ),
        }
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def apply_effects(self, effects: Dict):
        """应用选择效果"""
        for key, value in effects.items():
            if hasattr(self.player, key):
                current = getattr(self.player, key)
                new_value = max(0, min(100, current + value))
                setattr(self.player, key, new_value)
                
                # 显示变化
                if value > 0:
                    print(f"  ↗ {key}: +{value}")
                elif value < 0:
                    print(f"  ↘ {key}: {value}")
    
    def show_node(self, node: StoryNode):
        """显示故事节点"""
        self.clear_screen()
        print("\n" + "="*60)
        print(f"📖 {node.title}")
        print("="*60)
        print(node.content)
        print("\n" + "-"*60)
        print("💭 你的选择：")
        print("-"*60)
        
        for i, choice in enumerate(node.choices, 1):
            print(f"\n  {i}. {choice['text']}")
        
        print("\n" + "="*60)
    
    def get_choice(self, node: StoryNode) -> int:
        """获取玩家选择"""
        while True:
            try:
                choice = input(f"\n请输入选项 (1-{len(node.choices)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(node.choices):
                    return choice_num - 1
                else:
                    print("❌ 无效选项，请重新输入")
            except ValueError:
                print("❌ 请输入数字")
    
    def determine_ending(self) -> str:
        """确定结局"""
        p = self.player
        
        if p.controversy >= 90:
            return "ending_banned"
        elif p.controversy >= 70:
            return "ending_controversial"
        elif p.popularity >= 90 and p.capital >= 80:
            return "ending_top"
        elif p.talent >= 90 and p.popularity >= 95 and p.controversy < 30:
            return "ending_legend"
        elif p.talent >= 85 and p.controversy < 40:
            return "ending_artist"
        elif p.popularity >= 80 and p.loyalty < 30:
            return "ending_fade"
        elif p.capital < 30 and p.talent >= 70:
            return "ending_behind"
        else:
            return "ending_normal"
    
    def show_ending(self):
        """显示结局"""
        ending = self.determine_ending()
        
        endings = {
            "ending_legend": {
                "title": "🏆 S级结局：传奇巨星",
                "content": """
    你成为了华语乐坛的标志性人物。
    
    代表作《情人》《YOUNG》成为经典，
    你亲自创作的作品获得业内广泛认可，
    从偶像成功转型为真正的音乐人。
    
    你的演唱会场场爆满，
    粉丝从十几岁追到几十岁，
    成为一代人的青春记忆。
    
    🎉 恭喜达成完美结局！
                """
            },
            "ending_top": {
                "title": "⭐ A级结局：顶流偶像",
                "content": """
    你是现象级顶流，商业价值极高。
    
    代言接到手软，杂志封面常客，
    粉丝号召力惊人，数据战无不胜。
    
    虽然争议不断，但你依然是
    这个时代最具代表性的偶像之一。
    
    🔥 你是真正的流量之王！
                """
            },
            "ending_artist": {
                "title": "🎵 B级结局：实力派歌手",
                "content": """
    你选择了用作品说话。
    
    虽然流量不是最高，但圈内口碑极佳，
    音乐作品质量上乘，获得专业认可。
    
    你有一群死忠歌迷，
    他们爱你的音乐，而不是你的数据。
    
    🎤 音乐人，用作品征服听众！
                """
            },
            "ending_controversial": {
                "title": "⚡ C级结局：争议明星",
                "content": """
    黑红也是红。
    
    你身上永远不缺争议和话题，
    喜欢的人很喜欢，讨厌的人很讨厌。
    
    商业价值依然很高，
    但路人缘一般，口碑两极分化。
    
    💥 争议是你最好的流量密码。
                """
            },
            "ending_fade": {
                "title": "🌅 D级结局：昙花一现",
                "content": """
    曾经红极一时，如今归于平淡。
    
    选秀带来的热度没有持续，
    没有核心作品支撑，粉丝逐渐流失。
    
    现在的你偶尔参加商演，
    或者转型直播带货。
    
    📉 娱乐圈，就是这么残酷。
                """
            },
            "ending_banned": {
                "title": "🚫 E级结局：被封杀退圈",
                "content": """
    负面事件爆发，舆论不可挽回。
    
    代言全部解约，作品被下架，
    社交账号被封，演出活动取消。
    
    你不得不退出娱乐圈，
    曾经的一切仿佛一场梦。
    
    💔 成也流量，败也流量。
                """
            },
            "ending_behind": {
                "title": "🎬 F级结局：转型幕后",
                "content": """
    聚光灯不再，但你没有离开音乐。
    
    你转型成为音乐制作人，
    为新人写歌、制作专辑。
    
    虽然不再站在台前，
    但你的作品通过别人继续发光。
    
    🎹 幕后英雄，另一种精彩。
                """
            },
            "ending_normal": {
                "title": "📘 普通结局：平淡人生",
                "content": """
    你的偶像之路平平无奇。
    
    没有大红大紫，也没有彻底失败，
    就像大多数参加过选秀的年轻人一样，
    最终被时代遗忘。
    
    但至少，你追逐过梦想。
    
    🌊 人海浮沉，各自安好。
                """
            }
        }
        
        ending_data = endings.get(ending, endings["ending_normal"])
        
        print("\n" + "="*60)
        print(ending_data["title"])
        print("="*60)
        print(ending_data["content"])
        print("\n" + "="*60)
        print("📊 最终属性：")
        self.player.show()
    
    def play(self):
        """主游戏循环"""
        self.clear_screen()
        print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🌟 《偶像之路：CXK 传奇》 🌟                          ║
    ║                                                          ║
    ║     一款基于真实出道历程的文字冒险游戏                    ║
    ║                                                          ║
    ║     "梦想是陪我睡觉的东西，不实现它我会失眠。"            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
        """)
        
        input("\n按 Enter 开始游戏...")
        
        while self.current_node != "final_ending":
            node = self.story_nodes.get(self.current_node)
            
            if not node:
                print(f"❌ 错误：找不到节点 {self.current_node}")
                break
            
            # 显示节点
            self.show_node(node)
            
            # 显示当前属性
            self.player.show()
            
            # 获取选择
            choice_idx = self.get_choice(node)
            choice = node.choices[choice_idx]
            
            # 应用效果
            if choice.get("effect"):
                print("\n📈 属性变化：")
                self.apply_effects(choice["effect"])
            
            # 记录历史
            self.history.append({
                "node": self.current_node,
                "choice": choice["text"]
            })
            
            # 进入下一节点
            self.current_node = choice["next"]
            
            if self.current_node == "final_ending":
                input("\n按 Enter 查看结局...")
                self.show_ending()
                break
            
            input("\n按 Enter 继续...")
        
        # 游戏结束
        print("\n" + "="*60)
        print("🎮 游戏结束")
        print("="*60)
        print("\n感谢游玩《偶像之路：CXK 传奇》！")
        print("\n💡 提示：不同的选择会导向不同的结局，")
        print("   再次游玩可以尝试不同的路线！")
        
        # 保存记录
        self.save_game()
    
    def save_game(self):
        """保存游戏记录"""
        save_data = {
            "player": asdict(self.player),
            "history": self.history,
            "ending": self.determine_ending()
        }
        
        filename = f"cxk_game_save_{random.randint(1000, 9999)}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 游戏记录已保存到: {filename}")


def main():
    """主函数"""
    game = CXKGame()
    
    while True:
        game.play()
        
        print("\n" + "-"*60)
        replay = input("\n是否再次游玩？(y/n): ").strip().lower()
        if replay != 'y':
            print("\n👋 再见！")
            break
        
        # 重新开始
        game = CXKGame()


if __name__ == "__main__":
    main()
