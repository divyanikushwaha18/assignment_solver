# Assignment 4: Web Scraping

## 1. Import HTML to Google Sheets

**Question:** What is the total number of ducks across players on page number 18 of ESPN Cricinfo's ODI batting stats?

**Answer:** 143

## 2. Scrape IMDb movies

**Question:** What is the JSON data for movies with ratings between 3 and 5 from IMDb?

**Answer:**
```json
[
  {
    "id": "tt9603060",
    "title": "1. Star Trek: Section 31",
    "year": "2025",
    "rating": "3.8"
  },
  {
    "id": "tt22475008",
    "title": "2. Watson",
    "year": "2024– ",
    "rating": "4.6"
  },
  {
    "id": "tt32214413",
    "title": "3. The Wedding Banquet",
    "year": "2025",
    "rating": "4.4"
  },
  {
    "id": "tt22804850",
    "title":  "4. Au-delà des vagues",
    "year": "2024",
    "rating": "4.7"
  },
  {
    "id": "tt7787524",
    "title": "5. Henry Danger: The Movie",
    "year": "2025",
    "rating": "5.0"
  },
  {
    "id": "tt10128846",
    "title": "6. Megalopolis",
    "year": "2024",
    "rating": "4.8"
  },
  {
    "id": "tt2322441",
    "title": "7. Cinquante nuances de Grey",
    "year": "2015",
    "rating": "4.2"
  },
  {
    "id": "tt4978420",
    "title": "8. Borderlands",
    "year": "2024",
    "rating": "4.6"
  },
  {
    "id": "tt32359602",
    "title": "9. Going Dutch",
    "year": "2025– ",
    "rating": "5.0"
  },
  {
    "id": "tt28637027",
    "title": "10. Into the Deep",
    "year": "2025",
    "rating": "3.3"
  },
  {
    "id": "tt31456973",
    "title": "11. Alarum",
    "year": "2025",
    "rating": "3.3"
  },
  {
    "id": "tt29929565",
    "title": "12. Opus",
    "year": "2025",
    "rating": "4.1"
  },
  {
    "id": "tt10886166",
    "title": "13. 365 jours",
    "year": "2020",
    "rating": "3.3"
  },
  {
    "id": "tt12262202",
    "title": "14. The Acolyte",
    "year": "2024",
    "rating": "4.2"
  },
  {
    "id": "tt20247888",
    "title": "15. Emmanuelle",
    "year": "2024",
    "rating": "4.3"
  },
  {
    "id": "tt31790441",
    "title": "16. Blindspår",
    "year": "2025– ",
    "rating": "4.9"
  },
  {
    "id": "tt4113114",
    "title": "17. Innocence volée",
    "year": "2015",
    "rating": "5.0"
  },
  {
    "id": "tt15041836",
    "title": "18. Werewolves",
    "year": "2024",
    "rating": "4.4"
  },
  {
    "id": "tt1340094",
    "title": "19. The Crow",
    "year": "2024",
    "rating": "4.7"
  },
  {
    "id": "tt1273235",
    "title": "20. A Serbian Film",
    "year": "2010",
    "rating": "4.9"
  },
  {
    "id": "tt27165670",
    "title": "21. Sugar Baby",
    "year": "2024",
    "rating": "4.5"
  },
  {
    "id": "tt11057302",
    "title": "22. Madame Web",
    "year": "2024",
    "rating": "4.0"
  },
  {
    "id": "tt1522157",
    "title": "23. Maskhead",
    "year": "2009",
    "rating": "3.4"
  },
  {
    "id": "tt1467304",
    "title": "24. The Human Centipede (First Sequence)",
    "year": "2009",
    "rating": "4.4"
  },
  {
    "id": "tt3605418",
    "title": "25. Knock Knock",
    "year": "2015",
    "rating": "4.9"
  }
]
```

## 3. Wikipedia Outline

**Question:** What is the URL of your API endpoint for retrieving Wikipedia outlines?

**Answer:** http://127.0.0.1:8000/api/outline

## 4. Scrape the BBC Weather API

**Question:** What is the JSON weather forecast description for Chicago?

**Answer:** 
```json
{
  "2025-02-08": "Light cloud and a gentle breeze",
  "2025-02-09": "Sunny intervals and a gentle breeze",
  "2025-02-10": "Sunny intervals and a gentle breeze",
  "2025-02-11": "Light snow and a moderate breeze",
  "2025-02-12": "Light snow and a moderate breeze",
  "2025-02-13": "Sunny intervals and a moderate breeze",
  "2025-02-14":  "Sunny intervals and a gentle breeze",
  "2025-02-15":  "Light snow and a gentle breeze",
  "2025-02-16": "Sleet and a moderate breeze",
  "2025-02-17": "Sunny intervals and a gentle breeze",
  "2025-02-18": "Light snow and light winds",
  "2025-02-19": "Heavy snow and a gentle breeze",
  "2025-02-20":  "Light snow and a gentle breeze",
  "2025-02-21": "Light cloud and a gentle breeze"
}
```

## 5. Find the bounding box of a city

**Question:** What is the maximum latitude of the bounding box of Santiago in Chile on the Nominatim API?

**Answer:** -33.4255888

## 6. Search Hacker News

**Question:** What is the link to the latest Hacker News post mentioning Go having at least 77 points?

**Answer:** https://devblogs.microsoft.com/go/go-1-24-fips-update/

## 7. Find newest GitHub user

**Question:** When was the newest GitHub user in Chennai with over 130 followers created?

**Answer:** 2023-07-10T05:30:12Z

## 8. Create a Scheduled GitHub Action

**Question:** Create a scheduled GitHub action that runs daily and adds a commit to your repository.

**Answer:** https://github.com/divyanikushwaha18/devsync-auto-update

## 9. Extract tables from PDF

**Question:** What is the total Maths marks of students who scored 21 or more marks in Maths in groups 77-100?

**Answer:** 39087

## 10. Convert a PDF to Markdown

**Question:** What is the markdown content of the PDF, formatted with prettier@3.4.2?

**Answer:** 
```markdown
# conicio appello tardus

| conicio | appello | tardus |
| ------- | ------- | ------ |
| dapifer | convoco | temeritas |
| suggero | capto | contra |
| labore | provident | crustulum |
| ascit | celo | dignissimos |

## Tot copia aedificium textus conicio

| sulumubi | absens | cedo |
| --------- | ------- | ---- |
| allatus | curriculum | arto conscendo |
| tamen | comis | appositus color |
| curis | succedo | casus aer |

> saepe auctor ventus ipsam absque
> eos cilicium usque stultus

> Thalassinus currus quaerat venia umquam deporto

> Vorago atrocitas depopulo claustrum crudelis perspiciatis pax urbanus asper.

- copiose cuius
- cimentarius ceno cariosus
- aspernatur aetas denego ago
- cui vinitor terminatio cognatus conitor
- considero carmen
- titulus sollers aequitas enim facilis
- bonus animi suggero
- veniam succurro stella virga volup
- textor cognomen suscipio ex
- quidem armarium amor sol
- apparatus illum textor suggero abeo
- suscipio subito

| taedium | volutabrum | tergo | veniam |
| ------- | ---------- | ----- | ------- |
| tremo | valde | adhuc | optio |
| valeo | depulso | atque | capio |
| cognomen | vivo | aequus | decipio |
| tondeo | credo | aro | dedecor |
| victus | maiores | claro | crinis |
| mollitia | spargo |
| sulum | tricesimus |
| magni | pecus |
| fugit | ducimus |
| aedificium | denego |
| reiciendis | viscus |

## Uredo in vinum ipsa angustus

- arto deripio clam voveo
- adsidue corrigo appositus
- conor decretum
- corona versus
- adfero temperantia causa
- asperiores triumphus
- advoco thorax
- vado culpo
- cultellus attero minus coadunatio velociter

> Currus alioqui carus somnus.

> curtus textus sustineo vere minima
> [cumque artificiose](cumque%20artificiose)

```
Vix cado casso demo territo.
Vulgivagus aqua cimentarius commodi pel ocer clarus nostrum.
Consuasor ago cultura cubitum valeo.
Depopulo aestus decens cetera infit articulus angulus cur libero cattus.
```

- conservo pauci
- veniam quae victoria
- reiciendis apostolus sto
- bis delibero voluptatibus
```
