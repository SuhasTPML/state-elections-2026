# Assam GeoJSON vs Wikipedia (2026) Verification

## Finalized Status Update (2026-03-05)

This project now uses finalized Assam and Kerala constituency map data aligned to Wikipedia naming/reference for 2026 workflow.

### Assam (Finalized)

- Finalized source in app: `data/svg/ASSAM_2023_keyed.svg`
- Constituency numbering/name mapping finalized to the provided 1-126 key and verified against Assam 2026 wiki constituency names list.
- District metadata is embedded in the keyed SVG (`data-district` for all 126 constituencies).
- Reference: https://en.wikipedia.org/wiki/2026_Assam_Legislative_Assembly_election

### Kerala (Finalized)

- Finalized files:
  - `data/geojson/KERALA_ASSEMBLY.geojson`
  - `data/geojson/KERALA_ASSEMBLY_optimized.geojson`
- `AC_NO -> AC_NAME` mapping aligned to the 2026 Kerala wiki candidate constituency ordering.
- AC 87 geometry was dissolved into a single polygon (internal split removed), and district kept as `ERNAKULAM`.
- Reference: https://en.wikipedia.org/wiki/2026_Kerala_Legislative_Assembly_election
- Generated on: 2026-03-05 10:40 UTC
- Wikipedia source: https://en.wikipedia.org/wiki/2026_Assam_Legislative_Assembly_election
- Local GeoJSON: `C:\Users\suhas.bhandari\Downloads\Claude\Experiments\Elections\data\geojson\ASSAM_ASSEMBLY_optimized.geojson`

## Summary

- GeoJSON polygons: **133**
- GeoJSON unique AC numbers: **126**
- Wikipedia unique AC numbers parsed: **126**
- Missing AC numbers in GeoJSON: **0**
- Missing AC numbers in Wikipedia parse: **0**
- AC-number-wise name mismatches: **125** / 126
- Name-set overlap (normalized, ignoring AC no): **80** / 126
- Names only in GeoJSON: **46**
- Names only in Wikipedia: **46**

## Interpretation

- Seat count aligns at 126 unique constituencies, but constituency naming/number mapping does not align with the 2026 page.
- This indicates the GeoJSON is not directly aligned to the 2026 constituency naming scheme used on Wikipedia (likely delimitation/renaming differences).

## Name Mismatch Samples (by AC No.)

| AC No | GeoJSON name | Wikipedia 2026 name |
|---|---|---|
| 1 | Ratabari | Gossaigaon |
| 2 | Patharkandi | Dotma (ST) |
| 3 | Karimganj North | Kokrajhar (ST) |
| 4 | Karimganj South | Baokhungri |
| 5 | Badarpur | Parbatjhora |
| 6 | Hailakandi | Golakganj |
| 7 | Katlicherra | Gauripur |
| 8 | Algapur | Dhubri |
| 9 | Silchar | Birsing Jarua |
| 10 | Sonai | Bilasipara |
| 11 | Dholai | Mankachar |
| 12 | Udharbond | Jaleshwar |
| 13 | Lakhipur | Goalpara West (ST) |
| 14 | Barkhola | Goalpara East |
| 15 | Katigora | Dudhnai (ST) |
| 16 | Haflong | Abhayapuri |
| 17 | Bokajan | Srijangram |
| 18 | Howraghat | Bongaigaon |
| 19 | Diphu | Sidli-Chirang (ST) |
| 20 | Baithalangso | Bijni |
| 21 | Mankachar | Bhowanipur-Sorbhog |
| 22 | Salmara South | Mandia |
| 23 | Dhubri | Chenga |
| 24 | Gauripur | Barpeta (SC) |
| 25 | Golakganj | Pakabetbari |
| 26 | Bilasipara West | Bajali |
| 27 | Bilasipara East | Chamaria |
| 28 | Gossaigaon | Boko-Chaygaon (ST) |
| 29 | Kokrajhar West | Palasbari |
| 30 | Kokrajhar East | Hajo-Sualkuchi |
| 31 | Sidli | Rangiya |
| 32 | Bongaigaon | Kamalpur |
| 33 | Bijni | Dispur |
| 34 | Abhayapuri North | Dimoria (SC) |
| 35 | Abhayapuri South | New Guwahati |
| 36 | Dudhnai | Guwahati Central |
| 37 | Goalpara East | Jalukbari |
| 38 | Goalpara West | Barkhetri |
| 39 | Jaleswar | Nalbari |
| 40 | Sorbhog | Tihu |

## Names only in GeoJSON (normalized)

- ABHAYAPURI NORTH
- ABHAYAPURI SOUTH
- ALGAPUR
- AMGURI
- BADARPUR
- BAGHBAR
- BAITHALANGSO
- BARAMA
- BARKHETRY
- BARKHOLA
- BATADROBA
- BHABANIPUR
- BILASIPARA EAST
- BILASIPARA WEST
- BOKO
- CHABUA
- CHAPAGURI
- CHAYGAON
- DHARMAPUR
- GAUHATI EAST
- GAUHATI WEST
- HAJO
- JALESWAR
- JAMUNAMUKH
- JANIA
- KALAIGAON
- KATIGORA
- KATLICHERRA
- KOKRAJHAR EAST
- KOKRAJHAR WEST
- LAHOWAL
- MAHMARA
- MANGALDOI
- MARIGAON
- MORAN
- NOWGONG
- PANERY
- PATACHARKUCHI
- RATABARI
- SALMARA SOUTH
- SARUKHETRI
- SIDLI
- SOOTEA
- SORBHOG
- THOWRA
- TITABAR

## Names only in Wikipedia 2026 page (normalized)

- ABHAYAPURI
- ALGAPUR KATLICHERRA
- AMRI
- BAJALI
- BAKSA
- BAOKHUNGRI
- BARKHETRI
- BHERGAON
- BHOWANIPUR SORBHOG
- BILASIPARA
- BINNAKANDI
- BIRSING JARUA
- BOKO CHAYGAON
- BORKHOLA
- CHABUA LAHOWAL
- CHAMARIA
- DEMOW
- DIMORIA
- DOTMA
- GORESHWAR
- GUWAHATI CENTRAL
- HAJO SUALKUCHI
- JALESHWAR
- KATIGORAH
- KHOWANG
- KOKRAJHAR
- MAHMORA
- MAKUM
- MANAS
- MANDIA
- MANGALDAI
- MORIGAON
- NADAUR
- NAGAON BATADRABA
- NEW GUWAHATI
- PAKABETBARI
- PARBATJHORA
- RAM KRISHNA NAGAR
- RONGKHANG
- RONGONADI
- SIDLI CHIRANG
- SISSIBORGAON
- SRIJANGRAM
- TANGLA
- TIHU
- TITABOR
## Full Constituency Lists (Manual Review)

### GeoJSON constituencies (ASSAM_ASSEMBLY_optimized.geojson)

001. Ratabari
002. Patharkandi
003. Karimganj North
004. Karimganj South
005. Badarpur
006. Hailakandi
007. Katlicherra
008. Algapur
009. Silchar
010. Sonai
011. Dholai
012. Udharbond
013. Lakhipur
014. Barkhola
015. Katigora
016. Haflong
017. Bokajan
018. Howraghat
019. Diphu
020. Baithalangso
021. Mankachar
022. Salmara South
023. Dhubri
024. Gauripur
025. Golakganj
026. Bilasipara West
027. Bilasipara East
028. Gossaigaon
029. Kokrajhar West
030. Kokrajhar East
031. Sidli
032. Bongaigaon
033. Bijni
034. Abhayapuri North
035. Abhayapuri South
036. Dudhnai
037. Goalpara East
038. Goalpara West
039. Jaleswar
040. Sorbhog
041. Bhabanipur
042. Patacharkuchi
043. Barpeta
044. Jania
045. Baghbar
046. Sarukhetri
047. Chenga
048. Boko
049. Chaygaon
050. Palasbari
051. Jalukbari
052. Dispur
053. Gauhati East
054. Gauhati West
055. Hajo
056. Kamalpur
057. Rangiya
058. Tamulpur
059. Nalbari
060. Barkhetry
061. Dharmapur
062. Barama
063. Chapaguri
064. Panery
065. Kalaigaon
066. Sipajhar
067. Mangaldoi
068. Dalgaon
069. Udalguri
070. Majbat
071. Dhekiajuli
072. Barchalla
073. Tezpur
074. Rangapara
075. Sootea
076. Biswanath
077. Behali
078. Gohpur
079. Jagiroad
080. Marigaon
081. Laharighat
082. Raha
083. Dhing
084. Batadroba
085. Rupohihat
086. Nowgong
087. Barhampur
088. Samaguri
089. Kaliabor
090. Jamunamukh
091. Hojai
092. Lumding
093. Bokakhat
094. Sarupathar
095. Golaghat
096. Khumtai
097. Dergaon
098. Jorhat
099. Majuli
100. Titabar
101. Mariani
102. Teok
103. Amguri
104. Nazira
105. Mahmara
106. Sonari
107. Thowra
108. Sibsagar
109. Bihpuria
110. Naoboicha
111. Lakhimpur
112. Dhakuakhana
113. Dhemaji
114. Jonai
115. Moran
116. Dibrugarh
117. Lahowal
118. Duliajan
119. Tingkhong
120. Naharkatia
121. Chabua
122. Tinsukia
123. Digboi
124. Margherita
125. Doom Dooma
126. Sadiya

### Wikipedia constituencies (2026 Assam page)

001. Gossaigaon
002. Dotma (ST)
003. Kokrajhar (ST)
004. Baokhungri
005. Parbatjhora
006. Golakganj
007. Gauripur
008. Dhubri
009. Birsing Jarua
010. Bilasipara
011. Mankachar
012. Jaleshwar
013. Goalpara West (ST)
014. Goalpara East
015. Dudhnai (ST)
016. Abhayapuri
017. Srijangram
018. Bongaigaon
019. Sidli–Chirang (ST)
020. Bijni
021. Bhowanipur–Sorbhog
022. Mandia
023. Chenga
024. Barpeta (SC)
025. Pakabetbari
026. Bajali
027. Chamaria
028. Boko–Chaygaon (ST)
029. Palasbari
030. Hajo–Sualkuchi
031. Rangiya
032. Kamalpur
033. Dispur
034. Dimoria (SC)
035. New Guwahati
036. Guwahati Central
037. Jalukbari
038. Barkhetri
039. Nalbari
040. Tihu
041. Manas
042. Baksa (ST)
043. Tamulpur (ST)
044. Goreshwar
045. Bhergaon
046. Udalguri (ST)
047. Majbat
048. Tangla
049. Sipajhar
050. Mangaldai
051. Dalgaon
052. Jagiroad (SC)
053. Laharighat
054. Morigaon
055. Dhing
056. Rupohihat
057. Kaliabor
058. Samaguri
059. Barhampur
060. Nagaon–Batadraba
061. Raha (SC)
062. Binnakandi
063. Hojai
064. Lumding
065. Dhekiajuli
066. Barchalla
067. Tezpur
068. Rangapara
069. Nadaur
070. Biswanath
071. Behali (SC)
072. Gohpur
073. Bihpuria
074. Rongonadi
075. Naoboicha (SC)
076. Lakhimpur
077. Dhakuakhana (ST)
078. Dhemaji (ST)
079. Sissiborgaon
080. Jonai (ST)
081. Sadiya
082. Doom Dooma
083. Margherita
084. Digboi
085. Makum
086. Tinsukia
087. Chabua–Lahowal
088. Dibrugarh
089. Khowang
090. Duliajan
091. Tingkhong
092. Naharkatia
093. Sonari
094. Mahmora
095. Demow
096. Sibsagar
097. Nazira
098. Majuli (ST)
099. Teok
100. Jorhat
101. Mariani
102. Titabor
103. Golaghat
104. Dergaon
105. Bokakhat
106. Khumtai
107. Sarupathar
108. Bokajan (ST)
109. Howraghat (ST)
110. Diphu (ST)
111. Rongkhang (ST)
112. Amri (ST)
113. Haflong (ST)
114. Lakhipur
115. Udharbond
116. Katigorah
117. Borkhola
118. Silchar
119. Sonai
120. Dholai (SC)
121. Hailakandi
122. Algapur–Katlicherra
123. Karimganj North
124. Karimganj South
125. Patharkandi
126. Ram Krishna Nagar (SC)

### Manual Fuzzy Match (Geo -> Wikipedia)

Notes:
- This is a manual fuzzy review by name similarity and known renaming/merge patterns.
- It is not an official delimitation mapping.

| GeoJSON name | Closest Wikipedia name | Confidence | Reason |
|---|---|---|---|
| Abhayapuri North | Abhayapuri | High | North/South split appears collapsed on wiki side |
| Abhayapuri South | Abhayapuri | High | North/South split appears collapsed on wiki side |
| Algapur | Algapur-Katlicherra | High | Combined constituency naming |
| Amguri | Demow | Medium | Likely renaming/replacement in same belt |
| Badarpur | Ram Krishna Nagar (SC) | Medium | Neighboring replacement in Barak valley |
| Baghbar | Mandia | Medium | Likely reshuffle in Barpeta region |
| Baithalangso | Amri (ST) | Medium | Hill/ST area replacement |
| Barama | Baksa (ST) | Medium | BTC-area renaming/restructuring |
| Barkhetry | Barkhetri | High | Spelling variant |
| Barkhola | Borkhola | High | Spelling variant |
| Batadroba | Nagaon-Batadraba | High | Merged/extended naming |
| Bhabanipur | Bhowanipur-Sorbhog | High | Expanded combined name |
| Bilasipara East | Bilasipara | High | East/West collapsed |
| Bilasipara West | Bilasipara | High | East/West collapsed |
| Boko | Boko-Chaygaon (ST) | High | Combined constituency naming |
| Chabua | Chabua-Lahowal | High | Combined constituency naming |
| Chapaguri | Dotma (ST) | Low | Probable BTC-area replacement, weak by name |
| Chaygaon | Boko-Chaygaon (ST) | High | Combined constituency naming |
| Dharmapur | Nadaur | Medium | Likely regional reshuffle |
| Gauhati East | New Guwahati | Medium | Guwahati-area renaming/split |
| Gauhati West | Guwahati Central | Medium | Guwahati-area renaming/split |
| Hajo | Hajo-Sualkuchi | High | Combined constituency naming |
| Jaleswar | Jaleshwar | High | Spelling variant |
| Jamunamukh | Binnakandi | Medium | Hojai-region replacement |
| Jania | Chamaria | Medium | Barpeta-region replacement |
| Kalaigaon | Tangla | Medium | Udalguri-region replacement |
| Katigora | Katigorah | High | Spelling variant |
| Katlicherra | Algapur-Katlicherra | High | Combined constituency naming |
| Kokrajhar East | Kokrajhar (ST) | High | East/West collapsed |
| Kokrajhar West | Kokrajhar (ST) | High | East/West collapsed |
| Lahowal | Chabua-Lahowal | High | Combined constituency naming |
| Mahmara | Mahmora | High | Spelling variant |
| Mangaldoi | Mangaldai | High | Spelling variant |
| Marigaon | Morigaon | High | Spelling variant |
| Moran | Khowang | Medium | Dibrugarh belt replacement |
| Nowgong | Nagaon-Batadraba | Medium | Renamed/merged old Nagaon naming |
| Panery | Bhergaon | Low | Same broader belt, weak lexical match |
| Patacharkuchi | Bajali | High | Patacharkuchi area represented as Bajali |
| Ratabari | Ram Krishna Nagar (SC) | Medium | Barak valley replacement |
| Salmara South | Mankachar | Medium | South Salmara-Mankachar consolidation |
| Sarukhetri | Bhowanipur-Sorbhog | Medium | Likely combined reconstitution |
| Sidli | Sidli-Chirang (ST) | High | Expanded combined name |
| Sootea | Nadaur | Low | Likely regional replacement; weak lexical match |
| Sorbhog | Bhowanipur-Sorbhog | High | Combined constituency naming |
| Thowra | Demow | Medium | Sivasagar belt replacement |
| Titabar | Titabor | High | Spelling variant |


