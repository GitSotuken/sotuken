import PySimpleGUI as sg
from checkFunction import checkLan


def check():
    layout = [
        [sg.Text(checkLan.checkLan())],
        [sg.Button("お使いの無線LANの簡易セキュリティチェック", key="check")],
        [sg.Button("閉じる")]
    ]

    window = sg.Window("お使いの無線LANルーターの情報", layout)
    while True:
        event, value = window.read()

        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break
        elif event == "check":
            checkVulnerability()

    window.close()


def checkConnect():
    layout = [
        [sg.Text(checkLan.network_scanner(),font=(15),justification="left")],
        [sg.Button("脆弱性診断",key="check")],
        [sg.Button("KRACK脆弱性診断",key="krack")],
        [sg.Button("閉じる")]
    ]

    window = sg.Window("無線LANルーターに接続している機器", layout, resizable=True)
    while True:
        event, value = window.read()

        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break
        elif event == "scan":
            scan(value["ip"])
        elif event == "check":
            result()
        elif event == "krack":
            krackTestForm()
        
    window.close()


def checkVulnerability():
    layout = [
        [sg.Text(checkLan.checkCrypted(),font=(20))],
        [sg.Button("閉じる")]
    ]

    window = sg.Window("簡易セキュリティチェック", layout, resizable=True)

    while True:
        event, value = window.read()

        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break

    window.close()


def scan(ip):
    layout = [
        [sg.Text(checkLan.portScan(ip))],
        [sg.Button("閉じる")]
    ]
    window = sg.Window("ポートスキャン結果", layout, resizable=True)

    while True:
        event, value = window.read()

        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break

    window.close()
    
    
def result():
    header = ["IP","MAC","ssh_open","ssh_pass","telnet_open","telnet_pass"]

    # layout = [
    #     [sg.Text(checkLan.vulnerabilityResult(),font=(199))],
    #     [sg.Button("閉じる")]
    # ]
    # window = sg.Window("脆弱性調査結果",layout,resizable=True)
    lis = checkLan.vulnerabilityResult()
    
    l = lis

    L = [[sg.Table(l,headings=header,font=(14))]]

    window = sg.Window("脆弱性調査結果",L,resizable=True)
    
    while True:
        event,value = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break
        
    window.close()

def krackTestForm():
    layout = [
        [sg.Text("調査したい端末のMACアドレスを入力してください"),sg.InputText(key="mac"),sg.Button("検証する",key="krack")]
    ]
    window = sg.Window("Krack脆弱性調査",layout,resizable=True)
    
    while True:
        event,value = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break
        elif event == "krack":
            krack_test(value["mac"])

        
    window.close()
    
def krack_test(mac):
    layout = [
        [sg.Text(checkLan.krack_script(mac))],
        [sg.Button("閉じる")]
    ]
    window = sg.Window("KRACK脆弱性調査結果",layout,resizable=True)
    
    while True:
        event,value = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "閉じる":
            break
        
    window.close()

"""
ここから初期画面
"""
sg.theme("DarkAmber")


layout = [
    [sg.Button("お使いの無線LANルーターの情報を表示する", key="check")],
    [sg.Button("無線LANルーターに接続している機器を表示する", key="connect")],
    [sg.Button("終了")]
]

window = sg.Window("ネットワーク診断", layout, resizable=True)

while True:
    event, value = window.read()

    if event == "check":
        check()

    if event == "connect":
        checkConnect()

    if event == sg.WIN_CLOSED or event == "終了":
        break

window.close()
