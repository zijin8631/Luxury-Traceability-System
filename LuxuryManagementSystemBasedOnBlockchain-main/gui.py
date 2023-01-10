import PySimpleGUI as sg
import cli
from block_chain import BlockChain
from xmlrpc.client import ServerProxy
import source_item

sg.theme('DarkBrown1')

"""Initialization"""
bc = BlockChain()
s = ServerProxy("http://localhost:9999")
parser = cli.new_parser()
args = parser.parse_args()
"""Structure"""


# 界面布局，将会按照列表顺序从上往下依次排列，二级列表中，从左往右依此排列
wallets_list = ["Click the button and show your address"]
balance_in_address = "Display the belonging in your wallet"
chain_details = "Display Chain Details"
initial_balance_text = "Please input a address or select one from the list"
transactionStatus = 'Your transaction status'

button1_CreateWallet = '1.Create a Wallet'
button2_PrintWallet = '2.Print Wallets'
button3_CheckWallet = '3.Check Wallet'
button4_Deliver = '4.Delivery'
button5_CheckBeloning = '5.Check Belonging'
button6_PrintChain = '6.Print Chain'

layout = [
    [sg.Button(button1_CreateWallet,size=(15,1)), sg.InputText('Your new address',size=(40,1),key="wallet_address"),
    sg.Button(button2_PrintWallet,size=(15,1)), sg.InputCombo(size=(40,5),values=wallets_list, key='walletlist')],
    [sg.Button(button3_CheckWallet,size=(15,1)), sg.InputText(initial_balance_text, size=(40,1), key='balanceText',enable_events=True),
    sg.Text(balance_in_address, key="balanceAddress")],

    [sg.Text("---------------------------------------------------------------------------------------------------------"
             "-----------------------------------------------------------------------")],
    [sg.Button(button4_Deliver,size=(15,1))],
    [sg.InputText('Sender',size=(40,1),key='sendAddr'),sg.InputText('Receiver',size=(40,1),key='recAddr'),
                        sg.InputText('itemid',size=(20,1),key='amount')],
    [sg.Text(transactionStatus, key="txstatus")],
    [sg.Text("----------------------------------------------------------------------------------------------------------"
             "----------------------------------------------------------------------")],

    [sg.Button(button5_CheckBeloning, size=(15, 1)), sg.InputText('Input itemid',size=(10,1),key='checkBelonging'),
     sg.Text("Item belongings", key="belongingInfo")],
    [sg.Button(button6_PrintChain, size=(15, 1)), sg.Multiline(chain_details, size=(100, 6), key=chain_details)],
    [sg.Button('Mine a Genesis Block(Only Press Once!)'), sg.Button('Quit')]
]

# 创造窗口
window = sg.Window('Luxury Management Blockchain Demo', layout)
# 事件循环并获取输入值
while True:
    client = cli.Cli()
    event, values = window.read()
    if event in (None, 'Quit'):   # 如果用户关闭窗口或点击`Cancel`
        break

    if event == 'Mine a Genesis Block(Only Press Once!)':
        Gaddr = client.create_genesis_block()
        window["wallet_address"].update(Gaddr)

    if event == button1_CreateWallet:
        try:
            new_address = client.create_wallet()
        except:
            new_address = "Error occurred in Creating Wallet!"
        window["wallet_address"].update(new_address)

    if event == button2_PrintWallet:
        new_wallet_list = client.print_all_wallet()
        window['walletlist'].update(values=new_wallet_list, set_to_index=0)

    if event == button3_CheckWallet:
        selected_address = ''
        balance = 0
        if values['balanceText'] != '' and values['balanceText'] != initial_balance_text:
            selected_address = values['balanceText']
            balance = client.get_balance(selected_address)
        elif values['walletlist'] != "" and values['walletlist'] != wallets_list[0]:
            selected_address = values['walletlist']
            balance = client.get_balance(selected_address)
        else:
            tempstring = 'Invalid input!'
            window["balanceAddress"].update(tempstring)
            continue
        balance_str = ('%s have a item %d' % (selected_address, balance))
        window["balanceAddress"].update(balance_str)

    if event == button4_Deliver:
        try:
            print(values['sendAddr'],values['recAddr'],values['amount'])
            response = client.send(values['sendAddr'],values['recAddr'],int(values['amount']))
            # twice to check once
            response,txdetails = client.send(values['sendAddr'],values['recAddr'],int(values['amount']))
            window['txstatus'].update(response)
            window[chain_details].update("Transfer id is: "+ txdetails.txid)
        except Exception as e:
            print(e)
            window['txstatus'].update('Exception occurred')
        # printStr =

    if event == button5_CheckBeloning:
        try:
            item_id = int(values['checkBelonging'])
            last_address = source_item.find_belonging(item_id)[1]
            display = "Item {} belongs to {}".format(item_id,last_address)
        except:
            display = "Invalid input"
        window["belongingInfo"].update(display)

    if event == button6_PrintChain:
        item_id = int(values['checkBelonging'])
        sourceInfo = source_item.source_chain(item_id)
        display = ''
        for info in sourceInfo:
            display = display + info[0] +" in "+ info[1]
            display = display +"\n"
        window[chain_details].update(display)



window.close()

