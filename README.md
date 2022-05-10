## Projektas drabužiai

5400 nuotraukų su 20 skirtingų kategorijų drabužiais:

<img src="https://repository-images.githubusercontent.com/296936930/66951d00-fabe-11ea-823a-cfdec51c055e" /> 


### Duomenys

`images.csv` failas apima:

* `image` - nuotraukos vardas
* `sender_id` - asmens, prisidėjusio prie nuotraukos gavimo, ID
* `label` - drabužio kategorijos pavadinimas
* `kids` - `True`, jei drabužis yra vaikiškas

### Nuoroda į duomenų rinkinį

* Daugiau informacijos apie duomenis: https://medium.com/data-science-insider/clothing-dataset-5b72cd7c3f1f

### Pasirinktas modelis

Pasirinktas jau ištreniruotas modelis Mobile Net V3, nes pačios parašyti
modeliai nedavė tokių gerų rezultatų, kaip ištreniruotas su daugybe
duomenų modelis. Pasirinkta V3, naujausia, Mobile Net modelio versija.
Bandytas ir V2 modelis, bet V3 buvo geresnis.

Atrinkta 10 didžiausių drabužių kategorijų. Testinių duomenų modelio 
tikslumas apie 84%. Su 5 kategorijomis tikslumas buvo beveik 94%,
tai pridėjus daugiau duomenų, modelis prognozuoja 10% blogiau.

#### Modelio metrikos su 10 drabužių kategorijų:

- Duomenys skaidomi į 15 batch'ų
- 


