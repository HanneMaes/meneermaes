// wacht tot de DOM volledig geladen is
document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("enterDungeon").addEventListener("click", function() {
    // als we op de 'Enter Dungeon' knop klikken voeren we de code hieronder uit

        // testen om het klikken op de knop werkt
        console.log('Enter Dungeon button clicked');

        // hide startpage
        document.getElementById('startpage').classList.add('hide'); 

        /* ********************* */
        /* generate random enemy */
        /* ********************* */

        /* RANDOM NAAM */

        // lijst met namen waaruit we een willekeurige naam gaan nemen
        let allNames = ['Kugg Dragonflame', 'Griglol Hellfist', 'Krukzakk Brightdeath', 'Makdokk Bloodstriker'];

        // een naam kiezen uit de lijst
        let nameNumber = Math.floor(Math.random() * allNames.length); // kies een willekeurig getal tussen 0 en het aantal namen in allNames
        let enemyName = allNames[nameNumber]; // maak een variabele aan met de nieuwe naam fS
        console.log('enemyName:', enemyName); // in developer tools laten zien wat de naam is

        // variabele aanmaken waarin de de HTML gaan oplsaan die we straks op de pagina gaan tonen
        let enemyHTML = '<h1 class="enemyName">' + enemyName + '</h1>';

        /* RANDOM STATS */

        // random strength tussen 1 en 10
        let enemyStrength = Math.floor(Math.random() * 10) + 1;
        console.log('enemyStrength:', enemyStrength); // in developer tools laten zien wat de strength is

        // random health tussen 50 en 100
        let enemyHealth = Math.floor(Math.random() * 51) + 50;
        console.log('enemyHealth:', enemyHealth); // in developer tools laten zien wat de health is

        // health en strength toevoegen aan de HTML code
        enemyHTML += '<div class="health">❤ ️Health: ' + enemyHealth + '</div><div class="strength">🗡 ️Strength: ' + enemyStrength + '</div>';

        /* RANDOM AFBEELING */

        // de afbeeldingen van de enemies zijn: "enemy1.jpg" tot en met "enemy6.jpg""
        // we starten met een random getal te genereren tussen 1 en 6 (omdat de afbeeldingen gaan van 1 tot en met 6)
        let enemyImageNumber = Math.floor(Math.random() * 6) + 1;

        // daarna maken de de naam van de afbeelding: "enemy" + random nummer + ".jpg" = enemy5.jpg
        let enemyImage = 'enemy' + enemyImageNumber + '.jpg';
        console.log('enemy image:', enemyImage); // controle of de naam van de afbeelding correct is

        // voeg de html voor de afbeelding toe aan de variable die de HTML code bevat
        enemyHTML += '<img class="enemyImage round" src="images/' + enemyImage + '">';

        // voeg de HTML code toe aan het juiste element in index.html
        let enemyElement = document.getElementById('enemy'); // omdat we dit element meerdere keren nodig hebben is het efficiënter om het op te slaan in een variabelen
        enemyElement.innerHTML = enemyHTML; // voeg de HTML code toe aan het element
        enemyElement.classList.remove('hide'); // toon het HTML element

        /* *************************************** */
        /* haal de hero gegevens uit het formulier */
        /* *************************************** */

        // maak een variabele aan voor de HTML-code van de hero
        let heroHTML = '';

        /* NAAM */

        // haal de naam uit het tekstveld
        let heroName = document.getElementById("naamTextfield").value;
        console.log('heroName:', heroName);

        /* CLASS */

        // welke radio button class optie is er gekozen?
        let heroClass = document.querySelector('input[name="classRadioButton"]:checked').value;
        console.log('heroClass:', heroClass);

        heroHTML += '<h1 class="heroName">' + heroName + ' <small>' + heroClass + '</small></h1>';

        /* STATS */

        let heroHealth;
        let heroStrength;

        // alle classes hun eigen stats geven
        if ( heroClass == 'Barbarian' ) {
            heroHealth = 60;
            heroStrength = 70;
        } else if ( heroClass == 'Paladin' ) {
            heroHealth = 130;
            heroStrength = 30;
        } else {
            // als het niet barbarian is, en niet paladin, dan moet het medic zijn
            heroHealth = 100;
            heroStrength = 50;
        }
        console.log('heroHealth:', heroHealth);
        console.log('heroStrength:', heroStrength);

        // health en strength toevoegen aan de HTML code
        heroHTML += '<div class="health">❤ ️Health: ' + heroHealth + '</div><div class="strength">🗡 ️Strength: ' + heroStrength + '</div>';

        /* VOEG DE HTML CODE TOE AAN DE PAGINA */

        // voeg de HTML code toe aan het juiste element in index.html
        let heroElement = document.getElementById('hero'); // omdat we dit element meerdere keren nodig hebben is het efficiënter om het op te slaan in een variabelen
        heroElement.innerHTML = heroHTML; // voeg de HTML code toe aan het element

        // alle HTML code is gegenereerd, toon nu het verborgen element
        heroElement.classList.remove('hide'); // toon het HTML element
        document.getElementById('vs').classList.remove('hide'); // toon het HTML element
    }); 
});
