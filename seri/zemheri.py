# MASAL DEĞİL — ZEMHERİ (10 bölüm)
# Gizli anlatıcı: Selim Hoca (önceki öğretmen). Final ters köşe: anlatıcının kendisi "çağıran"dır.
# Her bölüm: shots = [(sahne_şablonu, {parametreler}, "anlatım")]  — anlatım boşsa sahne sessiz/efektli akar.

SERI = "ZEMHERİ"
HESAP = "@masaldegill"

EP = []

EP.append(dict(no=1, ad="İlk Gece", shots=[
 ("hook", {}, "Gece biri adını üç kere seslense... cevap verir miydin? Düşünmeden söyleme. Çünkü Karlıdere'de bu sorunun yanlış cevabı yok. Sadece... geç kalınmış cevabı var."),
 ("village", {}, "Zemheri ayıydı. Kırk gecenin en uzunu. Emre, kar yüzünden üç gün gecikerek geldiği bu dağ köyüne, yeni öğretmen olarak atanmıştı."),
 ("muhtar_door", {}, "Muhtar onu lojmana kadar götürdü. Kapıda durdu. Gözlerini Emre'nin gözlerinden hiç ayırmadan, tek bir şey söyledi."),
 ("muhtar_door", {"zoom": 1}, "[whispering] Gece adını üç kere çağırırlarsa... sakın cevap verme. Ne olursa olsun. Kim olursa olsun."),
 ("desk", {"knock": 1}, "Emre güldü. Köy yeri, dedi, batıl inanç. Saat üçü on iki geçene kadar güldü. Sonra kapı çalındı. Üç kere."),
 ("door_in", {"call": "mom1"}, "Ses... annesinin sesiydi. Altı yüz kilometre uzaktaki annesinin."),
 ("profile", {"call": "mom2"}, "Emre nefesini tuttu. Kapıya bir adım attı. Sonra muhtarın gözlerini hatırladı."),
 ("window", {"slam": 1}, "Üçüncü kez çağırmadı. Pencereye vurdu."),
 ("prints", {}, "Sabah kapının önünde izler vardı. İnsan izi değildi. Ve kapının tahtasına, içeriden değil, dışarıdan... bir rakam kazınmıştı."),
 ("carved", {"text": "1"}, "Bir. Emre o gün bilmiyordu. Ama bu bir sayımdı. Ve sayım... kırka kadar sürecekti."),
], son="Kapıya kazınan sayı ne anlama geliyor? Yarın gece 00.00'da 2. bölüm."))

EP.append(dict(no=2, ad="Boş Sıra", shots=[
 ("hook_text", {"text": "2. BÖLÜM\nBOŞ SIRA"}, "Kırk gecenin ikinci sabahı. Emre ilk dersine girdi."),
 ("classroom", {}, "Sınıfta yedi çocuk vardı. Ve sekiz sıra. En arkadaki sıra boştu. Ama üstünde... tebeşir tozu yoktu. Biri her gün siliyordu onu."),
 ("paper", {"lines": ["YOKLAMA DEFTERİ", "1. Zeynep ✓", "2. Mehmet ✓", "3. Ayşe ✓", "...", "8. Selim Öğretmen", "CEVAP VERME!"]}, "Yoklama defterini açtı. Yedi isim tanıdıktı. Sekizinci satırda bir öğretmenin adı yazıyordu. Selim. Ve yanında, kırmızı kalemle: cevap verme."),
 ("classroom", {"zoom": 1}, "Emre o ismi yüksek sesle okudu. Selim. Sınıf bir anda sustu. En öndeki kız, Zeynep, gözünü kırpmadan fısıldadı."),
 ("girl", {}, "[whispering] Hocam... onun adını söylemeyin. Bir kere söylediniz. İki kere daha söylerseniz... gelir."),
 ("desk", {}, "O gece Emre uyuyamadı. Saat üçü on iki geçe, sobanın arkasındaki tahta oynadı. Altından, nemli, kalın bir defter çıktı."),
 ("paper", {"lines": ["Selim'in defteri", "Bu köyde kimse ölmüyor.", "Kimse doğmuyor.", "Her zemheri sadece...", "bir yabancı kayboluyor."]}, "Selim Hoca'nın defteriydi. İlk sayfada tek bir cümle vardı: Bu köyde kimse ölmüyor. Kimse doğmuyor. Her zemheri, sadece bir yabancı kayboluyor."),
 ("door_in", {"call": "mom1"}, "Ve tam o anda... kapının arkasından yine adını duydu."),
 ("carved", {"text": "2"}, "Sabah kapıda yeni bir çentik vardı. İki. Ama bu sefer altına başka bir şey kazınmıştı. Bir isim. Selim."),
], son="Selim Hoca'ya ne oldu? Defterin son sayfasında ne yazıyor? Yarın gece 00.00'da."))

EP.append(dict(no=3, ad="Selim'in Defteri", shots=[
 ("hook_text", {"text": "3. BÖLÜM\nSELİM'İN DEFTERİ"}, "Bir defter düşün. Senden önce burada yaşamış birinin son günlerini yazdığı. Ve her sayfası... sana yazılmış."),
 ("paper", {"lines": ["7. gece", "Kapıya annem geldi.", "Annem öleli on yıl oldu.", "Cevap vermedim."]}, "Yedinci gece, diye yazmıştı Selim. Kapıya annem geldi. Annem öleli on yıl oldu. Cevap vermedim."),
 ("paper", {"lines": ["21. gece", "Muhtar her sabah", "ipe bir düğüm atıyor.", "Kırk düğüm.", "Kırk gece."]}, "Yirmi birinci gece. Muhtar her sabah bir ipe düğüm atıyor. Kırk düğüm. Kırk gece. Neyi saydığını sordum. Gülümsedi."),
 ("profile", {}, "Emre sayfaları çevirdikçe elleri titredi. Çünkü Selim'in yazdığı her şey, ona bu üç gecede olanlarla aynıydı. Kelimesi kelimesine."),
 ("paper", {"lines": ["39. gece", "Bu gece üçüncüyü söyledi.", "Cevap vermedim.", "Ama biri cevap verdi.", "BENİM SESİMLE."]}, "Otuz dokuzuncu gece. Bu gece üçüncüyü söyledi. Cevap vermedim. Ama biri cevap verdi. Benim sesimle."),
 ("photo", {"year": "1987"}, "Defterin arasından bir fotoğraf düştü. Köy meydanı. Kalabalık. Arkasında tarih: Ocak, bin dokuz yüz seksen yedi."),
 ("photo", {"year": "1987", "zoom": 1}, "Emre fotoğrafa yakından baktı. En önde, elinde fenerle duran adam... muhtardı. Bugünkü yüzüyle. Bir gün bile yaşlanmamış."),
], son="Muhtar kim? 1987'de ne oldu? 4. bölüm yarın gece 00.00'da."))

EP.append(dict(no=4, ad="Muhtar", shots=[
 ("hook_text", {"text": "4. BÖLÜM\nMUHTAR"}, "Bazı kapılar ziyaret için değil, saklamak için yapılır. Muhtarın evi de öyleydi."),
 ("village", {}, "Dördüncü gün, muhtar köyde yokken Emre onun evine gitti. Kapı kilitli değildi. Karlıdere'de hiçbir kapı kilitli değildi. Çünkü kimse içeriden kaçmıyordu."),
 ("rope", {"knots": 4}, "Duvarda bir ip asılıydı. Üzerinde dört düğüm. Ve düğümlerin yanında, rafta... tozlu, metal isim levhaları."),
 ("plates", {"names": ["SELİM ÖĞRETMEN  2025", "HÜLYA ÖĞRETMEN  2024", "KADİR ÖĞRETMEN  2023", "NURİ ÖĞRETMEN  1987"]}, "Selim öğretmen. Hülya öğretmen. Kadir öğretmen. Her yıl bir isim. Her zemheri bir öğretmen. Ve en eskisi... bin dokuz yüz seksen yedi."),
 ("profile", {}, "Emre bir adım geri çekildi. Arkasındaki dolabın kapağına çarptı. Kapak açıldı. İçinde, kadife bir beze sarılı, yepyeni bir levha duruyordu."),
 ("plates", {"names": ["EMRE ÖĞRETMEN  2026"], "single": 1}, "Üzerinde, taze kazınmış harflerle... Emre öğretmen. İki bin yirmi altı."),
 ("muhtar_door", {}, "Arkasından bir ses geldi. Muhtar kapıdaydı. Elinde fener. Yüzünde, o hiç değişmeyen gülümseme."),
 ("muhtar_door", {"zoom": 1}, "[whispering] Erken bakmışsın hocam. Daha otuz altı gece var."),
], son="Levha neden şimdiden hazır? Emre kaçabilecek mi? 5. bölüm yarın gece 00.00'da."))

EP.append(dict(no=5, ad="Kaçış", shots=[
 ("hook_text", {"text": "5. BÖLÜM\nKAÇIŞ"}, "Kaçmak mümkün mü? Herkes bunu sorar. Asıl soru şu: Kaçtığın yer gerçekten var mı?"),
 ("road", {}, "Beşinci gece Emre çantasını aldı ve yürümeye başladı. On iki kilometre. İlçe yoluna kadar. Kar dizlerine kadardı."),
 ("road", {"lights": 1}, "Saat üçe doğru, karanlığın içinden iki far belirdi. Eski bir minibüs. Şoför camı indirdi, yüzüne uzun uzun baktı."),
 ("profile", {}, "Emre titreyerek anlattı. Karlıdere'den geliyorum, dedi. Şoför bir an sustu. Sonra güldü. Ama gözleri gülmüyordu."),
 ("ruins", {}, "Karlıdere mi? Orası bin dokuz yüz seksen yedide boşaltıldı oğlum. Bir zemheri gecesi. Kırk kişi... tek gecede kayboldu. Otuz dokuz yıldır orada kimse yaşamıyor."),
 ("road", {"empty": 1}, "Emre başını çevirdi. Minibüs yoktu. Far yoktu. İz yoktu. Sadece kendi ayak izleri vardı. Ve izler... köye doğru gidiyordu."),
 ("door_in", {}, "Gözlerini açtığında lojmandaydı. Çantası kapının önünde, kar içinde duruyordu. Ve kapıda yeni bir çentik vardı."),
 ("carved", {"text": "5"}, "Beş. Köy onu bırakmamıştı. Hiç bırakmamıştı."),
], son="Köy 39 yıldır boşsa, Emre'nin her gün gördüğü insanlar kim? 6. bölüm yarın gece 00.00'da."))

EP.append(dict(no=6, ad="Zeynep'in Resmi", shots=[
 ("hook_text", {"text": "6. BÖLÜM\nZEYNEP'İN RESMİ"}, "Çocuklar yalan söylemez derler. Ama bazen... doğruyu da sadece resim yaparak söyleyebilirler."),
 ("classroom", {}, "Emre ertesi gün derse girdi. Çocuklar yerlerindeydi. Sanki hiçbir şey olmamış gibi. Sanki bu köy otuz dokuz yıldır boş değilmiş gibi."),
 ("girl", {}, "Teneffüste Zeynep yanına geldi. Bir kâğıt uzattı. Hiçbir şey söylemedi. Sadece, kimse görmesin diye, kâğıdı ters tuttu."),
 ("drawing", {}, "Bir resimdi. Lojman. Kapıda Emre. Arkasında, boynuzlu, uzun kollu bir gölge. Ve köy meydanında... bütün köylüler. Ayaklarının yerinde, çatal toynaklar."),
 ("girl", {"zoom": 1}, "[whispering] Onlar da gelmişti hocam. Senin gibi. Onlar da cevap vermemişti."),
 ("classroom", {"shadow": 1}, "Emre başını kaldırdı. Güneş pencereden vuruyordu. Sınıfın duvarında yedi çocuğun gölgesi vardı. Altısı, çocuk gölgesiydi."),
 ("shadow", {}, "Yedincisi... Zeynep'in gölgesiydi. Ve başının üstünde, iki uzun... kıvrık... boynuz vardı."),
], son="Zeynep kim? Ve neden Emre'yi uyarıyor? 7. bölüm yarın gece 00.00'da."))

EP.append(dict(no=7, ad="Telefon", shots=[
 ("hook_text", {"text": "7. BÖLÜM\nTELEFON"}, "Köyde çekmeyen telefon, otuz birinci gece... çaldı."),
 ("desk", {}, "Otuz gün boyunca Emre her gece saydı. Her gece biri adını iki kere söyledi ve sustu. Her sabah kapıda yeni bir çentik. Otuz. Bir gece babası, bir gece çocukluk arkadaşı, bir gece... kendi sesi."),
 ("carved", {"text": "30"}, "Ama hiçbir gece üçüncüyü söylemediler. Sanki bekliyorlardı. Sanki doğru sesi arıyorlardı."),
 ("phone", {"caller": "Annem"}, "Ekranda tek kelime vardı. Annem. Emre titreyen parmaklarla açtı."),
 ("profile", {}, "Annesinin sesi ağlıyordu. Oğlum, dedi, sen ne yapıyorsun? Kırk gündür her gece... kapıma gelip adımı söylüyorsun."),
 ("profile", {"zoom": 1}, "Emre'nin kanı dondu. Ben buradayım anne, dedi. Karlıdere'deyim. Hiçbir yere gitmedim."),
 ("phone", {"caller": "Annem", "static": 1}, "Hat cızırdadı. Annesinin sesi bir anda sakinleşti. Çok sakin. Fazla sakin. Biliyorum oğlum, dedi. Ben de buradayım."),
 ("door_in", {}, "Kapının önünde... ayak sesleri."),
 ("door_in", {"call": "mom2"}, ""),
], son="Kapıdaki gerçekten annesi mi? 8. bölüm yarın gece 00.00'da."))

EP.append(dict(no=8, ad="Kapıdaki", shots=[
 ("hook_text", {"text": "8. BÖLÜM\nKAPIDAKİ"}, "En zor şey neydi biliyor musun? Korkunç bir sesi duymamak değil. Sevdiğin bir sesi duyup... kapıyı açmamak."),
 ("door_in", {}, "Emre o gece kapıyı açmadı. Annesi sabaha kadar ağladı. Üşüdüğünü söyledi. Ellerinin donduğunu söyledi. Emre kulaklarını tıkadı. Saydı. Sabah ezanına kadar saydı."),
 ("prints", {}, "Sabah kapıyı açtığında, karda annesinin ayak izleri vardı. Küçük, tanıdık izler. Kapıya kadar geliyordu."),
 ("prints", {"turn": 1}, "Ama geri dönen izler... insan izi değildi."),
 ("village", {}, "Köy meydanında herkes toplanmıştı. Kırk kişi. Hepsi ona bakıyordu. Muhtar öne çıktı. Elinde ip vardı. Otuz dokuz düğüm."),
 ("rope", {"knots": 39}, "[whispering] Aferin hocam. Kimse buraya kadar gelemedi. Selim bile. Bir gece kaldı."),
 ("muhtar_door", {}, "Ve muhtar ilk kez gülümsemedi. Fısıldadı: Yarın gece üçüncüsü gelecek. Cevap vermezsen... sen de bizden olursun."),
], son="Cevap vermemek kurtuluş mu, tuzak mı? 9. bölüm yarın gece 00.00'da."))

EP.append(dict(no=9, ad="Gerçek Kural", shots=[
 ("hook_text", {"text": "9. BÖLÜM\nGERÇEK KURAL"}, "Sana söylenen kuralı hatırlıyor musun? Adını üç kere çağırırlarsa cevap verme. Peki ya kural... ters söylendiyse?"),
 ("stove", {}, "Son gece. Emre Selim'in defterini sobaya atmak üzereydi. Ateş kapağı yaladı. Ve yanan cildin arasından, gizli bir sayfa ortaya çıktı."),
 ("paper", {"lines": ["GERÇEK KURAL", "Üç kere çağrıldığında", "cevap vermeyen...", "ÇAĞIRAN OLUR."], "burn": 1}, "Gerçek kural. Üç kere çağrıldığında cevap vermeyen... çağıran olur."),
 ("drawing", {}, "Her şey yerine oturdu. Köylüler. Toynaklar. Kırk kişi. Hepsi bir zamanlar cevap vermeyenlerdi. Muhtar dahil. Ve Selim... Selim de cevap vermemişti."),
 ("profile", {}, "Peki cevap verenler? Defterin son satırında yazıyordu: Cevap veren, zemheriyi bitirir. Ama bedeli... kimse bilmiyor."),
 ("door_in", {"call": "girl"}, "Saat üçü on iki geçe kapı çalındı. Bu sefer annesi değildi. Zeynep'ti. Ağlıyordu. Hocam, diyordu, ne olur cevap ver. Bizi de kurtar."),
 ("window", {}, "Bir. İki. Emre kapıya yürüdü. Elini kola koydu. Ve üçüncü çağrı geldi. Ama bu ses... ne annesinindi, ne Zeynep'in."),
], son="Üçüncü çağrıyı yapan kim? FİNAL yarın gece 00.00'da."))

EP.append(dict(no=10, ad="Cevap (Final)", shots=[
 ("hook_text", {"text": "FİNAL\nCEVAP"}, "On gecedir sana bu hikâyeyi anlatıyorum. Hiç merak ettin mi... anlatan kim?"),
 ("door_in", {}, "Üçüncü çağrı, kapının arkasından gelmiyordu. İçeriden geliyordu. Odanın içinden. Emre'nin kulağının dibinden."),
 ("reveal", {}, "Emre. Emre. Emre."),
 ("reveal", {"zoom": 1}, "Evet. Bendim. Selim. Senden önceki öğretmen. Cevap vermediğim için çağıran olan. On gecedir sana anlattığım her kelime... bir çağrıydı."),
 ("profile", {}, "Emre gözlerini kapattı. Ve hayatında hiç olmadığı kadar sakin bir sesle cevap verdi. Buradayım."),
 ("dawn", {}, "Güneş doğdu. Kırk gecedir ilk kez. Kar eriyordu. Lojman yoktu. Köy yoktu. Sadece otuz dokuz yıllık yıkıntılar. Ve karın üstünde kırk bir çift ayak izi. Hepsi insan izi. Hepsi... köyden dışarı gidiyordu."),
 ("ruins", {}, "Emre'yi o sabah yolda buldular. Yaşıyordu. Ama saçları... bembeyazdı. Kimseye hiçbir şey anlatmadı. Sadece bir şey sordu: Zemheri ne zaman başlıyor?"),
 ("hook", {"final": 1}, "Çünkü zemheri her yıl gelir. Ve bir çağıran her yıl... yeni birini bulur. Bu seriyi sonuna kadar izledin. Adını üç kere söylesem... cevap verir misin?"),
], son="SON. Bu hikâye bitti mi sence? Yorumlara yaz."))

ACIKLAMA = {
 1: "Gece biri adını üç kere seslense… cevap verir miydin? 🌑\n\nZEMHERİ · 1. Bölüm: İlk Gece\nKarlıdere köyüne atanan öğretmen Emre'ye muhtar tek bir kural söyledi. İlk gece kapı çalındı.\n\n👁 Kapıya kazınan sayı ne anlama geliyor? Tahminini yorumlara yaz.\n🔔 10 bölümlük seri — her gece 00.00'da yeni bölüm. Kaçırmamak için takip et.",
 2: "Sekiz sıra, yedi çocuk. Boş sırayı her gün kim siliyor? 🌑\n\nZEMHERİ · 2. Bölüm: Boş Sıra\nYoklama defterindeki sekizinci isim bir öğretmene aitti.\n\n👁 Selim Hoca'ya sence ne oldu? Yoruma yaz.\n⏮ 1. bölüm profilde · 🔔 Her gece 00.00'da yeni bölüm.",
 3: "Senden önce gelenin defteri… ve her sayfası sana yazılmış. 🌑\n\nZEMHERİ · 3. Bölüm: Selim'in Defteri\n1987'den bir fotoğraf. Ve hiç yaşlanmayan bir yüz.\n\n👁 Muhtar kim? Teorini yorumlara yaz.\n⏮ Önceki bölümler profilde · 🔔 Yarın gece 00.00.",
 4: "Raf dolusu isim levhası. En yenisinde… onun adı. 🌑\n\nZEMHERİ · 4. Bölüm: Muhtar\n\"Erken bakmışsın hocam. Daha otuz altı gece var.\"\n\n👁 Sence Emre kaçabilir mi? Evet/Hayır yaz.\n⏮ Önceki bölümler profilde · 🔔 Yarın gece 00.00.",
 5: "Kaçtığın yer gerçekten var mı? 🌑\n\nZEMHERİ · 5. Bölüm: Kaçış\nKarlıdere 1987'de boşaltıldı. Peki Emre'nin her gün gördüğü insanlar kim?\n\n👁 Teorini yorumlara yaz, en iyi tahmini sabitleyeceğiz.\n⏮ Önceki bölümler profilde · 🔔 Yarın gece 00.00.",
 6: "Çocuklar yalan söylemez. Ama doğruyu bazen sadece resimle söyleyebilirler. 🌑\n\nZEMHERİ · 6. Bölüm: Zeynep'in Resmi\nDuvarda yedi gölge vardı. Biri çocuk gölgesi değildi.\n\n👁 Zeynep iyi mi, kötü mü? Yorumda tartışalım.\n⏮ Önceki bölümler profilde · 🔔 Yarın gece 00.00.",
 7: "Çekmeyen telefon otuz birinci gece çaldı. Ekranda: Annem. 🌑\n\nZEMHERİ · 7. Bölüm: Telefon\n\"Kırk gündür her gece kapıma gelip adımı söylüyorsun.\"\n\n👁 Sen olsan kapıyı açar mıydın? Yoruma yaz.\n⏮ Önceki bölümler profilde · 🔔 Yarın gece 00.00.",
 8: "Korkunç bir sesi duymak değil… sevdiğin bir sesi duyup kapıyı açmamak. 🌑\n\nZEMHERİ · 8. Bölüm: Kapıdaki\nGelen izler insan iziydi. Giden izler değil.\n\n👁 Cevap vermemek kurtuluş mu, tuzak mı? Yorumlara yaz.\n⏮ Önceki bölümler profilde · 🔔 Yarın gece 00.00.",
 9: "Sana söylenen kural… ya ters söylendiyse? 🌑\n\nZEMHERİ · 9. Bölüm: Gerçek Kural\nÜç kere çağrıldığında cevap vermeyen… çağıran olur.\n\n👁 Üçüncü çağrıyı kim yaptı? Final öncesi son tahminini yaz.\n⏮ Önceki bölümler profilde · 🔔 FİNAL yarın gece 00.00.",
 10: "On gecedir sana bu hikâyeyi anlatıyorum. Hiç merak ettin mi… anlatan kim? 🌑\n\nZEMHERİ · FİNAL: Cevap\nBaştan izle, anlatıcının sesine dikkat et.\n\n👁 Ters köşeyi tahmin eden var mıydı? Yorumlara yaz.\n🔔 Yeni seri yakında — takipte kal.",
}
ETIKET = "#masaldeğil #zemheri #korku #gerilim #korkuhikayeleri #karakoncolos #anadolu #animasyon #reels #dizi"
