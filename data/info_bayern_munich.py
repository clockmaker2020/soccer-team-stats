import json
import os

# 팀명 설정 (다른 팀으로 변경 가능)
team_name = "Bayern München"
team_id = 157  # API에서 제공되는 팀 ID (예시)

# JSON 파일 경로
file_path = f"data/team_data/info_bayern_munich.json"

# 경기 데이터 예제 (실제 API 데이터를 대체해야 함)
match_data = {
    "fixture": {
        "id": 123456,  # 경기 ID (예시)
        "date": "2024-02-25T18:30:00Z",
        "venue": {
            "name": "Allianz Arena",
            "city": "Munich"
        },
        "referee": "Felix Zwayer"
    },
    "league": {
        "name": "Bundesliga",
        "season": 2024,
        "round": "Matchday 23"
    },
    "teams": {
        "home": {
            "id": team_id,
            "name": team_name,
            "logo": "https://example.com/bayern_logo.png"
        },
        "away": {
            "id": 165,
            "name": "Borussia Dortmund",
            "logo": "https://example.com/dortmund_logo.png"
        }
    },
    "score": {
        "halftime": {"home": 1, "away": 0},
        "fulltime": {"home": 3, "away": 1}
    },
    "events": [
        {"time": 12, "player": "Leroy Sané", "team": team_name, "detail": "Normal Goal"},
        {"time": 45, "player": "Joshua Kimmich", "team": team_name, "detail": "Yellow Card"},
        {"time": 78, "player": "Erling Haaland", "team": "Borussia Dortmund", "detail": "Normal Goal"}
    ],
    "statistics": {
        "ball_possession": "62% - 38%",
        "shots": {"total": [18, 9], "on": [9, 3]},
        "passes_accuracy": "87% - 81%",
        "corners": "6 - 4",
        "fouls": "10 - 12",
        "yellow_cards": "1 - 2",
        "red_cards": "0 - 0",
        "offsides": "2 - 1"
    },
    "lineups": {
        "home": {
            "coach": "Thomas Tuchel",
            "startingXI": ["Neuer", "Kimmich", "De Ligt", "Davies", "Sané", "Müller"],
            "substitutes": ["Ulreich", "Mazraoui", "Tel"]
        },
        "away": {
            "coach": "Edin Terzić",
            "startingXI": ["Kobel", "Hummels", "Reus", "Bellingham", "Haaland"],
            "substitutes": ["Meyer", "Schlotterbeck"]
        }
    },
    "odds": {
        "1X2": {"home": 1.75, "draw": 3.40, "away": 4.50},
        "handicap": "+1.5 Bayern",
        "over_under": "Over 2.5"
    },
    "past_results": [
        {"date": "2024-02-18", "score": "2-1 vs Bayer Leverkusen"},
        {"date": "2024-02-10", "score": "1-1 vs Leipzig"}
    ],
    "future_games": [
        {"date": "2024-03-02", "opponent": "RB Leipzig"},
        {"date": "2024-03-09", "opponent": "SC Freiburg"}
    ]
}

# 디렉토리 생성 (존재하지 않으면)
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# JSON 파일 저장
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(match_data, f, indent=4, ensure_ascii=False)

print(f"✅ {file_path} 파일이 성공적으로 생성되었습니다.")
