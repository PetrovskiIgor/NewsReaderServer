__author__ = 'igorpetrovski'

from model.Source import Source

sources = [
            Source(0, 'http://vecer.mk', ['http://vecer.mk/rss.xml']),#opoziconen
            Source(1,'http://www.crnobelo.com',['http://www.crnobelo.com/?format=feed&type=rss']),
            Source(2,'http://sitel.mk',['http://sitel.mk/rss.xml']),#opoziconen
            Source(3,'http://kurir.mk',['http://kurir.mk/feed/']),#opoziconen
            Source(4,'http://republika.mk',['http://republika.mk/?feed=rss2']),#opoziconen
            #Source(5,'http://plusinfo.mk',['http://plusinfo.mk/rss/biznis','http://plusinfo.mk/rss/skopje', 'http://plusinfo.mk/rss/kultura',
              #                 'http://plusinfo.mk/rss/zdravje', 'http://plusinfo.mk/rss/svet', 'http://plusinfo.mk/rss/scena']),
            Source(6,'http://www.vest.mk',['http://www.vest.mk/rssGenerator/']),#opoziconen
            Source(7,'http://alsat.mk',['http://alsat.mk/RssFeed']),
            Source(8,'http://www.mkd.mk/',[ 'http://www.mkd.mk/feed']),
            Source(9,'http://www.sport.com.mk',['http://www.sport.com.mk/rssgenerator/rss.aspx']),
            Source(10,'http://www.dnevnik.mk',['http://www.dnevnik.mk/rssGenerator/']),#opoziconen
            Source(11, 'http://interesno.com.mk' , ['http://interesno.com.mk/index.php?format=feed&type=rss' ]),
            Source(12, 'http://www.fakulteti.mk/',['http://www.fakulteti.mk/rss/rss.ashx']),
            Source(13, 'http://novatv.mk/', ['http://novatv.mk/feed']), # ne se load-a feedot
            Source(14, 'http://kajgana.com/', ['http://kajgana.com/rss.xml']),
            Source(15, 'http://derbi.mk/', ['http://derbi.mk/feed/']),
            Source(16, 'http://www.libertas.mk/', ['http://www.libertas.mk/feed/']),
            Source(17, 'http://mkd-news.com/', ['http://mkd-news.com/feed/']),
            Source(18, 'http://www.brif.mk/', ['http://www.brif.mk/feed/']),
            Source(19, 'http://off.net.mk/', ['http://feeds.feedburner.com/offnetmk']),
            Source(20, 'http://it.mk/', ['http://it.mk/feed/']),
            Source(21, 'http://www.smartportal.mk/',['http://www.smartportal.mk/feed/']),
            Source(22, 'http://popularno.mk/',['http://www.popularno.mk/feed/']),
            Source(23, 'http://www.femina.mk/',['http://www.femina.mk/rss']),
            Source(24, 'http://doktori.mk/',['http://feeds.feedburner.com/doktorimk']),
            Source(25, 'http://tocka.com.mk/',['http://tocka.com.mk/rss.php']),
            Source(26, 'http://koli.com.mk/',['http://koli.com.mk/rss.ashx']),
            Source(27, 'http://a1on.mk/wordpress/',['http://a1on.mk/wordpress/feed']),
            Source(28, 'http://reporter.mk/',['http://reporter.mk/feed/']),
            Source(29, 'http://lokalno.mk/',['http://lokalno.mk/feed/']),
            Source(30, 'http://automedia.mk/',['http://automedia.mk/?feed=rss2']),
            Source(31, 'http://netpress.com.mk/',['http://netpress.com.mk/feed/']),#opoziconen
            Source(32, 'http://evesti.mk/', ['http://feeds.feedburner.com/evesti']),
            Source(33, 'http://www.novamakedonija.com.mk/', ['http://www.novamakedonija.com.mk/rssAll.asp']),
            Source(34, 'http://makfax.com.mk/', ['http://makfax.com.mk/_feeds/rss2/news']),
            Source(35, 'http://ekonomski.mk/', ['http://ekonomski.mk/feed/']),
            Source(36, 'http://www.spektra.com.mk/', ['http://www.spektra.com.mk/rss']),
            Source(37, 'http://bi.mk/', ['http://bi.mk/feed/']),
            Source(38, 'http://faktor.mk/', ['http://faktor.mk/feed/']),
            Source(39, 'http://aktuelno24.mk/', ['http://feeds.feedburner.com/aktuelno24/ywvm']), #losho lista sliki,
            Source(40, 'http://pozitiv.mk/', ['http://pozitiv.mk/feed/']),
            Source(41, 'http://www.idividi.com.mk/', ['http://www.idividi.com.mk/rss.aspx']),
            Source(42, 'http://zase.mk/', ['http://zase.mk/feed/']), #ne raboti feedot koga vlecam od localhost

            # ----------- PROVERKA -----------------
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            Source(43, 'http://www.avtomagazin.com.mk/', ['http://www.avtomagazin.com.mk/avto-magazin.rss']), #PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(44, 'http://meta.mk/', ['http://meta.mk/feed/']), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(45, 'http://slobodna.mk/', ['http://slobodna.mk/feed/']), #PROVERENO TEKSTOT SE ZEMA DOBRO (NEKOGAS LISTA I META DATA)
            Source(47, 'http://www.utrinski.mk/', ['http://www.utrinski.mk/rssgenerator/rss.aspx']), # PROVERENO, TEKSTOT SE ZEMA DOBRO (samo naslovot se povtoruva duplo)
            Source(48, 'http://kapital.mk/', ['http://kapital.mk/feed/']), # LOSH FEED
            Source(49, 'http://www.akademik.mk/', ['http://www.akademik.mk/feed/']),# PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(50, 'http://mk.rbth.com/', ['http://mk.rbth.com/xml/index.xml'], 'Руска реч'),# PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(51, 'http://telma.com.mk/', ['http://telma.com.mk/rss.xml'], 'Телма'), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(52, 'http://kanal77.mk/', ['http://kanal77.mk/feed/']), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(53, 'http://24vesti.mk/', ['http://24vesti.mk/rss.xml']), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(54, 'http://marketing365.mk/', ['http://marketing365.mk/feed/']),# PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(55, 'http://maxim.mk/', ['http://maxim.mk/rss.xml']), # PROVERENO, TEKSTOT SE ZEMA DOBRO

            # PROVERENO, RAZLICNI TAGOVI. pr: entry mesto item itn
            # ako ima povekje vakvi slucaevi togas da se razmisli kako da se opfati ovoj slucaj (povtorno e mozhno so dictionaries)
            Source(56, 'http://prizma.birn.eu.com/', ['http://mix.chimpfeedr.com/5ee9b-Prizma'], 'Призма')
          ]



#the dictionary that tells us which paragraphs we need to ignore for a given source
fetch_text_specifications = {
                'http://vecer.mk/rss.xml':[0,-3],
                'http://www.crnobelo.com/?format=feed&type=rss': [0,-2],
                'http://novatv.mk/rss.xml?tip=2'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=5'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=7'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=23'   :[2,-2],
                'http://www.vest.mk/rssGenerator/'  :[0,-7],
                'http://alsat.mk/RssFeed'           :[1,-3],
                'http://www.mkd.mk/feed':{'tag_type':'div', 'attribute_type':'id', 'attribute_value':'main-wrapper',
                                            'nested_tag_type':'div', 'nested_attribute_type':'class', 'nested_attribute_value':'field-body',

                                             },

                'http://www.sport.com.mk/rssgenerator/rss.aspx': [1],
                'http://reporter.mk/feed/':[3,-10],
                'http://tocka.com.mk/rss.php':{'tag_type':'div', 'attribute_type':'id', 'attribute_value':'sodrzina_vest'},
                'http://www.femina.mk/rss':[0,-7],
                'http://feeds.feedburner.com/offnetmk':{'tag_type':'div', 'attribute_type':'class',
                                                        'attribute_value':['sodrzhina-full', 'voved']},
                'http://lokalno.mk/feed/': [0,-9],
                'http://it.mk/feed/':[2,-28],
                'http://netpress.com.mk/feed/': [0,-1],
                'http://feeds.feedburner.com/doktorimk':[1,-1],
                'http://feeds.feedburner.com/evesti': [0,-10],
                'http://makfax.com.mk/_feeds/rss2/news':[2,-5],
                'http://ekonomski.mk/feed/':[0,-4],
                'http://www.spektra.com.mk/rss':[0,-12],
                'http://bi.mk/feed/':[0,-23], #da se proveruva za update!!!,
                'http://faktor.mk/feed/': [0,-20],
                'http://pozitiv.mk/feed/': [0,-2],
                'http://www.motika.com.mk/feed/': [4],
                'http://www.idividi.com.mk/rss.aspx':[0,-13],
                'http://kurir.mk/feed/': [0,-5],
                'http://www.avtomagazin.com.mk/avto-magazin.rss':[0,-23],
                'http://slobodna.mk/feed/':{'tag_type':'div', 'attribute_type':'class', 'attribute_value':'entry clearfix'},
                'http://meta.mk/feed/':[1,-14],

                'http://maxim.mk/rss.xml':[0,-6],
                'http://marketing365.mk/feed/':[0,-21],
                'http://www.utrinski.mk/rssgenerator/rss.aspx': [3,-6],
                'http://telma.com.mk/rss.xml':[0,-1],
                'http://kanal77.mk/feed/':{'tag_type':'div', 'attribute_type':'class', 'attribute_value':'entry', 'nested_tag_type':'p',
                                           'nested_attribute_type':'class', 'nested_attribute_value': None},
                'http://www.akademik.mk/feed/':[0,-1],
                'http://mk.rbth.com/xml/index.xml':[0,-2],
                'http://www.avtomagazin.com.mk/avto-magazin.rss':{'tag_type':'section', 'attribute_type':'class', 'attribute_value':'link-arrow'},
                'http://24vesti.mk/rss.xml':{'tag_type':'div', 'attribute_type':'class', 'attribute_value':'main-content',
                                            'nested_tag_type':'div', 'nested_attribute_type':'class', 'nested_attribute_value':'content',
                                             'limit':1},
                'http://republika.mk/?feed=rss2':{'tag_type':'div', 'attribute_type':'id', 'attribute_value':'article_text'}
                }