import requests
import csv

# API 엔드포인트
NODE_API = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/TopisIccMsNode/1.0"
LINK_API = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/TopisIccMsLink/1.0"

# 인증키 등 필요한 파라미터는 실제 서비스에 맞게 추가하세요.
API_KEY = "6b5a2ce1-aeb8-4afa-a220-2ef4ea40c5ea"  # 실제 키로 교체

def fetch_node_data():
    try:
        params = {"apikey": API_KEY}
        response = requests.get(NODE_API, params=params)
        response.raise_for_status()
        data = response.json() # 실제 응답 구조에 맞게 수정
        with open("spot_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "nodeId",
                "nodeTypeCd",
                "nodeTypeNm",
                "turnPCd",
                "turnPNm",
                "grs80tmX",
                "grs80tmY",
                "x",
                "y",
                "nodeName"
            ])
            for node in data:
                writer.writerow([
                    node.get("nodeId"),
                    node.get("nodeTypeCd"),
                    node.get("nodeTypeNm"),
                    node.get("turnPCd"),
                    node.get("turnPNm"),
                    node.get("grs80tmX"),
                    node.get("grs80tmY"),
                    node.get("x"),
                    node.get("y"),
                    node.get("nodeName")
                ])
        print("지점 데이터 저장 완료")
    except Exception:
        print("지점 데이터를 가져오는데 실패했습니다.")


def fetch_link_data():
    try:
        params = {"apikey": API_KEY}
        response = requests.get(LINK_API, params=params)
        response.raise_for_status()
        data = response.json()  # 실제 응답 구조에 맞게 수정
        with open("section_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "roadName",
                "linkID",
                "stnodeID",
                "ednodeID",
                "stnodeNM",
                "ednodeNM",
                "mapDist",
                "stdLinkCnt",
                "bsRoadYn",
                "regCd",
                "regNm",
                "trfClsDivCd",
                "trfClsDivNm",
                "trfServYn"
            ])
            for link in data:
                writer.writerow([
                    link.get("roadName"),
                    link.get("linkID"),
                    link.get("stnodeID"),
                    link.get("ednodeID"),
                    link.get("stnodeNM"),
                    link.get("ednodeNM"),
                    link.get("mapDist"),
                    link.get("stdLinkCnt"),
                    link.get("bsRoadYn"),
                    link.get("regCd"),
                    link.get("regNm"),
                    link.get("trfClsDivCd"),
                    link.get("trfClsDivNm"),
                    link.get("trfServYn")
                ])
        print("구간 데이터 저장 완료")
    except Exception as e:
        print("구간 데이터를 가져오는데 실패했습니다.", e)


if __name__ == "__main__":
    fetch_node_data()
    fetch_link_data()
