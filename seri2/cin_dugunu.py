# MASAL DEĞİL — 2. SERİ: CİN DÜĞÜNÜ (10 bölüm)
# Mekân: Eski bir taş kervansaray ("Eski Han"), Mezopotamya'ya bakan taş bir şehir. Kış, perşembe gecesi.
# Ters köşe (final): Kerem'in "insan dünyası" yedi yıldır yok; düğün gecesi kaybolan damat oydu. Ayakları ters.
# Her satır: (KONUŞAN, "metin")  —  ANLATICI dış ses; diğerleri karakter sesi (ElevenLabs, ayrı ses).

SERI = "CİN DÜĞÜNÜ"
HESAP = "@masaldegill"

KADRO = {
 'ANLATICI':  dict(ad='Anlatıcı', ses='Nihat – The Timeless Voice', voice_id='MuOq11XzQTthwLhmGZ2V', tarif='Kadife, kalın, masalcı bariton. Yavaş, fısıltıya yakın.'),
 'KEREM':     dict(ad='Kerem (28)', ses='Sergin – Warm Narrator', voice_id='OP4UedUzNB5e2mktGvdT', tarif='Genç zurnacı. Borçlu, annesi hasta. Cesur ama korkusunu saklayamıyor.'),
 'RIZA':      dict(ad='Usta Rıza (70)', ses='yaşlı erkek sesi — ElevenLabs kütüphanesinden seçilecek', voice_id=None, tarif='Kerem’in davulcu ustası. Bilge görünüyor; kırk yıllık bir borcu var.'),
 'AGA':       dict(ad='Dünür Ağa', ses='Akay – The Cinematic Narrator', voice_id='XjeT2V2moeoWReDQKJU8', tarif='Siyahlar içinde, kibar, hiç gülmeyen gözler. Cinlerin şeyhi.'),
 'NAZLI':     dict(ad='Nazlı (25)', ses='İrem – Kadife Akustik', voice_id='hy7OAv1nH3Eqqj96Aude', tarif='Kerem’in çocukluk aşkı. Yedi yıl önce düğün gecesi kayboldu. Gelin.'),
 'ANA':       dict(ad='Hatice Ana (60)', ses='Zuhal – Turkish Narrator', voice_id='Xen0soH4tcGo78ododZU', tarif='Kerem’in annesi. Hasta, sıcak, dualı.'),
 'HACI':      dict(ad='Kör Hacı Baba (80)', ses='Celil – Turkish Narrator', voice_id='Zpbxhg6LG47cY8y5BJrf', tarif='Hanın kör bekçisi. Gözü görmez ama her şeyi bilir.'),
 'MIRCAN':    dict(ad='Mircan (cin çocuk)', ses='Deniz – Storyteller & Animation (perde yükseltilmiş)', voice_id='2w5twzryiFg9VNnXphRP', tarif='Şerbet dağıtan, gülümseyen küçük çocuk. Gözleri fazla büyük.'),
 'KAHVECI':   dict(ad='Kahveci Şükrü', ses='Yavuz Demir', voice_id='RTq4D78xGS1cikM2yy6C', tarif='Kahvehane sahibi, meraklı, korkak.'),
}

KURALLAR = ["Çaldığın havayı yarıda kesme.", "Sana sunulanı yeme, içme.", "Ayaklarına bakma.", "Adını kimseye söyleme."]

EP = []
EP.append(dict(no=1, ad="Davet", son="Altınların üstündeki tarih neden 1311? 2. bölüm yarın gece 00.00'da.", sahneler=[
 ("kahvehane_gece", [("ANLATICI","Sana kapının önünde biri, bir kese altın uzatsa... hiçbir şey sormadan alır mıydın? Kerem aldı. Çünkü annesinin ilacı... bir haftadır yarımdı.")]),
 ("kahvehane_ic", [("KAHVECI","Kerem, oğlum, bu ay da ödeyemezsen zurnanı rehin alırım, ona göre."),("KEREM","Şükrü abi, bir hafta. Bir düğün çıksın, hepsini öderim.")]),
 ("kahvehane_kapi", [("ANLATICI","Kapı açıldı. İçeri soğuk değil, bir koku girdi. Yanık tarçın ve ıslak toprak. Siyahlar giymiş, uzun boylu bir adam doğruca Kerem'in masasına yürüdü."),
                     ("AGA","Zurnacı Kerem sensin. Bu gece bir düğünümüz var. Eski Han'da. Gün doğana kadar çalacaksın.")]),
 ("masa_kese", [("ANLATICI","Masaya bir kese bıraktı. Kese açıldığında kahvehanedeki bütün mumlar bir anlığına eğildi."),
                ("KEREM","Eski Han mı? Orası yıkık, kimse gitmez oraya."),("AGA","Bu gece gidecekler. Ustanı da getir. Davul olmadan halay olmaz.")]),
 ("riza_ev", [("ANLATICI","Usta Rıza keseyi görünce elindeki çay bardağını düşürdü."),
              ("RIZA","Bu altınları sayma, Kerem. Sayarsan... geri alırlar."),("KEREM","Kim alır usta? Kim bunlar?"),
              ("RIZA","Sorma. Çalacağız. Gün doğunca da arkamıza bakmadan döneceğiz.")]),
 ("altin_yakin", [("ANLATICI","Ama Kerem o gece eve dönünce dayanamadı. Bir altını mumun ışığına tuttu. Altın... sıcaktı. İçinde kalp atıyormuş gibi. Ve üstünde bir tarih vardı: Bin üç yüz on bir.")]),
]))
EP.append(dict(no=2, ad="Kurallar", son="Misafirlerin ayakları neden ters? 3. bölüm yarın gece 00.00'da.", sahneler=[
 ("yol_han", [("ANLATICI","Gece yarısı. Eski Han'a giden yolda tek bir köpek bile havlamadı. Rıza davulunu sırtına almış, dua mırıldanıyordu. Kerem'in elinde zurna, cebinde o sıcak altın.")]),
 ("han_kapisi", [("ANLATICI","Hanın kapısında, elinde fenerle, kör bir ihtiyar bekliyordu. Hacı Baba. Gözleri bembeyazdı ama Kerem'e dosdoğru baktı."),
                 ("HACI","Hoş geldin zurnacı. İçeri girmeden önce dört şey söyleyeceğim. Kulağını aç.")]),
 ("hacı_yakin", [("HACI","Bir: çaldığın havayı yarıda kesme. İki: sana ne sunulursa sunulsun, yeme, içme. Üç: aşağı bakma. Ayaklarına bakma."),
                 ("KEREM","Dördüncüsü?"),("HACI","Adını... kimseye söyleme. Bu gece kimse adını bilmeyecek.")]),
 ("avlu_giris", [("ANLATICI","Kapı açıldı. Yıkık sandıkları han... ışıl ışıldı. Yüzlerce fener. Kadife minderler. Ve avlunun ortasında yüzlerce misafir. Hepsi dans ediyordu. Ama hiçbir ses yoktu. Ne bir ayak sesi. Ne bir kahkaha.")]),
 ("sahne_ust", [("AGA","Hoş geldiniz. Başlayın. Ve sakın durmayın."),("RIZA","Bismillah, oğlum. Bir... iki... üç...")]),
 ("calgi", [("ANLATICI","Zurna ötünce bütün avlu aynı anda döndü. Yüzlerce baş, aynı anda, Kerem'e baktı. Sonra halay başladı.")]),
 ("ayaklar", [("ANLATICI","Kerem kuralı biliyordu. Ama göz, insanın içinden kaçar. Bir an... sadece bir an aşağı baktı. Misafirlerin etekleri savruldu. Ve Kerem gördü: ayakların hepsi... tersti. Topukları önde, parmakları arkada.")]),
]))
EP.append(dict(no=3, ad="Gelin", son="Nazlı yedi yıl önce nereye kayboldu? 4. bölüm yarın gece 00.00'da.", sahneler=[
 ("calgi", [("ANLATICI","Kerem zurnayı bırakmadı. Nefesi kesildi ama bırakmadı. Rıza'nın davulu onu taşıyordu. Bir... iki... üç...")]),
 ("gelin_alayi", [("ANLATICI","Sonra avlunun öbür ucundan gelin alayı girdi. Kırmızı kadife. Altın kemer. Yüzünde kalın, al bir duvak. Misafirler iki yana çekildi.")]),
 ("gelin_yakin", [("ANLATICI","Gelin, sahnenin önünden geçerken durdu. Ve duvak... bir rüzgârla aralandı. Rüzgâr yoktu oysa.")]),
 ("kerem_yakin", [("ANLATICI","Kerem o yüzü tanıdı. Yedi yıl önce kendi düğün gecesi kaybolan, bütün köyün aradığı, kuyulara bakılan... Nazlı.")]),
 ("gelin_yakin", [("NAZLI","Kerem..."),("ANLATICI","Sesi çıkmadı. Sadece dudakları kıpırdadı. Tek bir kelime."),("NAZLI","Kaç.")]),
 ("sahne_ust", [("AGA","Gelinimizi beğendin mi zurnacı? Yedi yıldır bu geceyi bekliyor."),("KEREM","Kimi... kimi bekliyor?"),
                ("AGA","Damadını, elbette. Çal. Damat gelince görürsün.")]),
]))
EP.append(dict(no=4, ad="Ziyafet", son="Usta Rıza kimin tarafında? 5. bölüm yarın gece 00.00'da.", sahneler=[
 ("sofra", [("ANLATICI","Gece yarısını çoktan geçmişti. Avlunun kenarına sofralar kuruldu. Kuzu, pilav, irmik helvası. Kokusu insanın aklını alıyordu.")]),
 ("mircan", [("MIRCAN","Amca, susamışsın. Şerbet getirdim. Gül şerbeti. Annem yaptı."),("ANLATICI","Küçük bir çocuktu. Gülümsüyordu. Ama gözleri... bir çocuğun gözünden büyüktü. Ve hiç kırpmıyordu.")]),
 ("kerem_yakin", [("KEREM","Sağ ol, güzel kardeşim. İçmeyeyim."),("MIRCAN","Neden? Herkes içiyor. Bak, ustan bile içti.")]),
 ("riza_sofra", [("ANLATICI","Kerem başını çevirdi. Usta Rıza sofranın başına oturmuştu. Bir eliyle davulu çalıyor, öbür eliyle... yemek yiyordu. Ve gülümsüyordu. Kerem onu kırk yıl tanısa, böyle gülümsediğini görmemişti.")]),
 ("kerem_yakin", [("KEREM","Usta! Ne yapıyorsun? Hacı Baba ne dedi?"),("RIZA","Kural sizin için, evlat. Benim için değil. Ben... burada çok yedim.")]),
 ("golgeler", [("ANLATICI","Fenerlerin ışığı duvara vuruyordu. Bütün misafirlerin gölgeleri vardı. Ama Rıza'nın gölgesinde... ayak yoktu. Gölge dizlerinden aşağısı yokmuş gibi bitiyordu.")]),
]))
EP.append(dict(no=5, ad="Halay", son="Bu gece neden sabah olmuyor? 6. bölüm yarın gece 00.00'da.", sahneler=[
 ("calgi", [("ANLATICI","Halay hızlandı. Önce Kerem'in parmakları yandı. Sonra dudakları çatladı. Zurnanın kamışına kan bulaştı.")]),
 ("halay_genis", [("ANLATICI","Yüzlerce misafir el ele, omuz omuza. Halay başı mendil sallıyordu. Mendil kırmızıydı. Başta beyaz olduğuna Kerem yemin edebilirdi.")]),
 ("sahne_ust", [("AGA","Daha hızlı, zurnacı. Halay yavaşlarsa damat gelmez."),("KEREM","Saat kaç? Sabah olmadı mı hâlâ?"),("AGA","Burada saat yok. Sen durana kadar gece.")]),
 ("han_gok", [("ANLATICI","Kerem avlunun üstündeki göğe baktı. Yıldızlar... hiç kımıldamamıştı. Saatlerdir aynı yerdeydi. Ay da. Sanki biri geceyi bir yere çivilemişti.")]),
 ("kerem_yakin", [("ANLATICI","Ve uzaklardan, çok uzaklardan, Kerem bir ses duydu. Sabah ezanının ilk kelimesi. Allahu Ekber. Ama ikinci kelime... hiç gelmedi.")]),
 ("hacı_yakin", [("HACI","Ezanı duyuyorsan, hâlâ yarın senin, zurnacı. Duymaz olduğunda... sen de onlardansın.")]),
]))
EP.append(dict(no=6, ad="Ayna", son="Aynadaki kadın gerçekten annesi mi? 7. bölüm yarın gece 00.00'da.", sahneler=[
 ("calgi", [("ANLATICI","Rıza bir ara davulu hızlandırdı ve Kerem'e göz kırptı. Bu, ustasının eski işaretiydi: Ben tutarım, sen nefes al.")]),
 ("koridor", [("ANLATICI","Kerem zurnayı bir an Rıza'nın davuluna teslim edip avlunun arkasındaki dar koridora girdi. Yüzünü yıkamak istiyordu. Koridorun sonunda, eski bir hamam aynası vardı.")]),
 ("ayna", [("ANLATICI","Aynada kendi yüzü vardı. Yorgun, kanlı dudaklı. Ama arkasında, aynanın içinde, halay hâlâ dönüyordu. Ve halayın en ucunda, beyaz yazmasıyla...")]),
 ("ayna_yakin", [("ANA","Kerem... oğlum."),("KEREM","Anne? Anne, ne arıyorsun burada? Sen hastasın, yatağındasın!")]),
 ("ayna_yakin", [("ANA","Ben iyiyim oğlum. Hiç bu kadar iyi olmamıştım. Bak, ayaklarım ağrımıyor artık. Gel. Sen de gel.")]),
 ("kerem_yakin", [("ANLATICI","Kerem arkasını döndü. Koridor bomboştu. Sadece aynada... annesi hâlâ el sallıyordu. Ve aynadaki annesinin ayakları... tersti.")]),
]))
EP.append(dict(no=7, ad="Nazlı'nın Hikâyesi", son="Damat kim? 8. bölüm yarın gece 00.00'da.", sahneler=[
 ("koridor", [("NAZLI","Kerem. Bana bakma, zurnana bak. Bizi izliyorlar. Sadece dinle.")]),
 ("nazli_yakin", [("NAZLI","Yedi yıl önce, düğünümüzün gecesi, beni kapıda biri bekliyordu. Seni çağırdığını söyledi. Kuyunun başında beklediğini."),
                  ("KEREM","Ben seni bekledim Nazlı. Sabaha kadar. Bütün köy aradı."),("NAZLI","Biliyorum. Ben de seni duydum. Yedi yıl boyunca her perşembe... zurnanı duydum.")]),
 ("kerem_yakin", [("KEREM","Seni kim getirdi buraya? Kim?")]),
 ("nazli_yakin", [("NAZLI","Seni buraya getiren adam. Her yedi yılda bir. Bir gelin, bir çalgıcı. Bu gece de... bir damat lazım onlara."),("KEREM","Damat kim?")]),
 ("nazli_yakin", [("ANLATICI","Nazlı gözlerini Kerem'e kaldırdı. Yedi yıllık bir yorgunlukla. Ve en çok korktuğu cümleyi söyledi."),
                  ("NAZLI","Bu gece senin düğünün Kerem. Damat... sensin.")]),
]))
EP.append(dict(no=8, ad="Ustanın Borcu", son="Usta Rıza kim? 9. bölüm yarın gece 00.00'da.", sahneler=[
 ("calgi", [("ANLATICI","Kerem avluya döndü. Davul hâlâ çalıyordu. Ama Rıza'nın elleri artık davula değmiyordu. Davul kendi kendine çalıyordu.")]),
 ("riza_yakin", [("KEREM","Usta. Nazlı'yı sen mi getirdin buraya?"),("RIZA","Otur evlat. Zurnayı bırakma. Bırakma ki konuşabilelim.")]),
 ("riza_yakin", [("RIZA","Kırk yıl önce ben de senin gibiydim. Fakir. Aç. Bir gece siyahlı bir adam bana bir kese uzattı. Bin üç yüz on bir yılından altınlar."),
                 ("RIZA","Ben saydım, Kerem. Saydım. Ve her altın için... yedi yıl borçlandım.")]),
 ("kerem_yakin", [("KEREM","Nazlı'yı... borcunu ödemek için mi verdin?"),("RIZA","Nazlı bir taksitti. Sen... son taksitsin.")]),
 ("sahne_ust", [("AGA","Yeter, Rıza. Çok konuştun. Borcun bitti."),("ANLATICI","Ağa elini kaldırdı. Ve Rıza'nın yüzü... bir mum gibi erimeye başladı. Altından ne çıktı, Kerem bakamadı. Sadece kahkahayı duydu. Kırk yıldır tanıdığı ustasının sesi değildi bu.")]),
]))
EP.append(dict(no=9, ad="Son Hava", son="Kerem son notayı çalacak mı? FİNAL yarın gece 00.00'da.", sahneler=[
 ("calgi", [("ANLATICI","Artık davul yoktu. Usta yoktu. Sadece Kerem'in zurnası vardı ve yüzlerce ters ayak, onun etrafında dönüyordu.")]),
 ("hacı_yakin", [("HACI","Zurnacı. Kör olanın gözü daha iyi görür. Dinle beni. Bu düğün senin son havanla biter."),("KEREM","Son havayı çalarsam ne olur?"),
                 ("HACI","Düğün tamamlanır. Gelin damadına kavuşur. Sen onlardan olursun. Ama Nazlı... Nazlı nihayet uyur.")]),
 ("kerem_yakin", [("KEREM","Ya çalmazsam? Havayı yarıda kesersem?"),("HACI","İlk kuralı bozarsın. O zaman ne olacağını... kimse bilmez. Bilen de anlatmaya kalmadı.")]),
 ("gelin_yakin", [("NAZLI","Kerem. Benim için çalma. Ben yedi yıl bekledim. Bir yedi yıl daha beklerim.")]),
 ("sahne_ust", [("AGA","Çal, damat. Gelinin bekliyor. Annen bekliyor. Herkes seni bekliyor.")]),
 ("zurna_yakin", [("ANLATICI","Kerem zurnayı dudaklarına götürdü. Son havanın ilk notası çıktı. İkinci notası. Avlu sevinçle uludu. Ve üçüncü notadan önce... Kerem zurnayı dizinde kırdı.")]),
]))
EP.append(dict(no=10, ad="Sabah (Final)", son="SON.", sahneler=[
 ("han_sessiz", [("ANLATICI","Sessizlik. Yüzlerce fener aynı anda söndü. Misafirler yoktu. Ağa yoktu. Han yine yıkıktı. Ve gökte, ilk kez saatler sonra, yıldızlar kımıldadı.")]),
 ("ezan_safak", [("ANLATICI","Sabah ezanı okundu. Bu sefer sonuna kadar. Kerem kırık zurnasını alıp eve doğru yürüdü. Arkasına bakmadan. Rıza'nın dediği gibi.")]),
 ("ev_kapi", [("ANLATICI","Evin kapısını annesi açtı. Ayaktaydı. Yanakları pembeydi. Hiç hasta olmamış gibiydi."),
              ("KEREM","Anne... iyileşmişsin. Anne, bu gece ne oldu bilsen..."),("ANA","Kusura bakmayın evladım. Siz kimi aradınız?")]),
 ("ana_yakin", [("KEREM","Anne, benim. Kerem."),("ANA","Kerem mi? Benim oğlumun adı Kerem'di. Yedi yıl önce, düğün gecesi kayboldu. Gelinle birlikte. Hiç bulamadık.")]),
 ("kerem_ayak", [("ANLATICI","Kerem bir adım geri çekildi. Ve kuralı ilk kez kendi için bozdu. Aşağı baktı. Kendi ayaklarına.")]),
 ("kerem_ayak", [("ANLATICI","Topukları... öndeydi.")]),
 ("han_uzak", [("ANLATICI","O günden beri, her perşembe gecesi, Eski Han'dan bir zurna sesi gelir. Kırık bir zurna. Hep aynı havayı çalar. Ve hep... üçüncü notadan önce susar.")]),
 ("kapi_siyahli", [("ANLATICI","Eğer bir gece kapına siyahlar giymiş biri gelir de sana bir kese altın uzatırsa... Sakın sayma. Sakın adını söyleme. Bir de... ayaklarına bakma.")]),
]))

ACIKLAMA = {
 1: "Kapına biri bir kese altın uzatsa, hiçbir şey sormadan alır mıydın? 🌙\n\nCİN DÜĞÜNÜ · 1. Bölüm: Davet\nZurnacı Kerem'e Eski Han'da bir düğün teklif edildi. Ödeme: 1311 tarihli altınlar.\n\n👁 Sen olsan gider miydin? Yoruma yaz.\n🔔 10 bölümlük yeni seri — her gece 00.00'da yeni bölüm.",
}
ETIKET = "#masaldeğil #cindüğünü #korku #gerilim #korkuhikayeleri #cin #anadolu #animasyon #reels #dizi"
