import requests
from bs4 import BeautifulSoup



# İstanbul'da bulunan Pide ve lahmacun Restoranlarını Puanlarına göre sıralanmış sayfanın linkini girdim.
r = requests.get('https://www.yemeksepeti.com/istanbul/pide-lahmacun#sof:2|sob:true')



# Sayfayı bu şekilde görebiliriz ama öncelikle düzenlenmesi lazım.
#print(r.content)


# Veriler geldi, 200 yazması sayfanın başarılı bir şekilde indirildiğini gösteriyor.
#print(r)

# BeatifulSoup yardımı ile sayfayı parse ediyorum. Hızlı olduğu için lxml se
page = BeautifulSoup(r.content,'lxml')


'''
# Tüm restoranların bulunduğu div'i alıyorum.
restoranlar = page.find_all('div',attrs={'class':'ys-reslist-items'})
print(restoranlar)
for i in restoranlar:
    print(i.text)
'''





#Gerekli listeleri tanımlıyorum.
restoran_adi, restoran_linkleri, yorumSayisi, hiz, servis, lezzet, yorumlar_list = [] , [] , [] , [] , [] , [] , []


# Her bir restoranın bulunduğu div'i alıyorum.
restoran_dis = page.find_all('div',attrs={'class':'ys-item'})

counter, counter2 =0,0
for sayac,i in enumerate(restoran_dis):
    print(f"{sayac+1}.restoran")
    
    restoran_adi.append(i.find('a').text.strip())
    print('Restoran Adı: ',i.find('a').text.strip())
    
    restoran_linki = "https://www.yemeksepeti.com"+i.find('a')['href']
    print("Restoran Linki: ",restoran_linki)
    restoran_linkleri.append(restoran_linki)
    
    restoran_ic = requests.get(restoran_linki)
    restoran_ic = BeautifulSoup(restoran_ic.content,'lxml')
    
    try: 
        yorumSayisi.append(int(restoran_ic.find('a',attrs={'data-content-id':'restaurant_comments'}).text.strip('Yorumlar (').strip(')')))
        counter +=1
        print("Yorum sayisi: ",int(restoran_ic.find('a',attrs={'data-content-id':'restaurant_comments'}).text.strip('Yorumlar (').strip(')')))
    
    except:
        print('Bu restorana ait yorum yok.')
        yorumSayisi.append(0)
        print(restoran_linki)
        counter2+=1
        time.sleep(15)
    
    puan= restoran_ic.find('div',attrs={'class':'points'})
    
    try:
        #Puanları alıyorum.
        puanlar=puan.find_all('span')
    except AttributeError:
        print('\nRestoranlar bitti...')
        break
    
    # Puan verilmemiş restoranlarda hata vermemesi için try-except kullanıyorum.
    try:
        
        print(f"Puanlar:\nHız: {float(puanlar[1].text.replace(',','.'))}\nServis: {float(puanlar[3].text.replace(',','.'))}\nLezzet: {float(puanlar[5].text.replace(',','.'))}")
        kontrol=float(puanlar[1].text.replace(',','.'))+float(puanlar[3].text.replace(',','.'))+float(puanlar[5].text.replace(',','.'))
        #Puanları ayrıştırıp floata çeviriyorum.
        hiz.append(float(puanlar[1].text.replace(',','.')))
        servis.append(float(puanlar[3].text.replace(',','.')))
        lezzet.append(float(puanlar[5].text.replace(',','.')))
        
            
    except:
        print("Bu restorana ait değerlendirme puanı yok.\n")
        
        restoran_adi.pop()
        restoran_linkleri.pop()
        yorumSayisi.pop()
        
        continue
    
    # Yorumlara erişiyorum. 
    yorumlar = restoran_ic.find_all('div',attrs={'class':'comments-body'})
    
    
    # Yorumları toplamak için değişken oluşturuyorum.
    yorum_toplam=""
    
    # Yorumları for döngüsü ile topluyorum.
    for yorum in yorumlar:
        yorum_toplam += yorum.find('p').text
        
    yorumlar_list.append(yorum_toplam)    

    
    
    
    print("\n")
    



import pandas as pd


# DataFrame oluşturuyorum.
df = pd.DataFrame()


# Listeleri DataFrame'e aktarıyorum.
df['restoranAdi'] = restoran_adi
df['restoranLinki'] = restoran_linkleri
df['yorumSayisi'] = yorumSayisi
df['hizPuani'] = hiz
df['servisPuani'] = servis
df['lezzetPuani'] = lezzet
df['yorumlar'] = yorumlar_list


# DataFrame'i Excel'e yazıyorum.
df.to_excel('data3.xlsx')
