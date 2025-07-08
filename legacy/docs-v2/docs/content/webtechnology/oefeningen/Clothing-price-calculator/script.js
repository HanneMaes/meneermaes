// wacht tot de DOM volledig geladen is
document.addEventListener("DOMContentLoaded", function() {

	document.getElementById("calculate").addEventListener("click", function() {

		// haal de data
		var shirtManufacturing = document.getElementById("shirtManufacturing").value;
		var hoodyManufacturing = document.getElementById("hoodyManufacturing").value;
		var shipping = document.getElementById("shipping").value;
		var shirtSellingPrice = document.getElementById("shirtSellingPrice").value;
		var hoodySellingPrice = document.getElementById("hoodySellingPrice").value;
		var targetProfit = document.getElementById("targetProfit").value;

		console.log("shirtManufacturing:", shirtManufacturing);
		console.log("hoodyManufacturing:", hoodyManufacturing);
		console.log("shipping:", shipping);
		console.log("shirtSellingPrice:", shirtSellingPrice);
		console.log("hoodySellingPrice:", hoodySellingPrice);
		console.log("targetProfit:", targetProfit);
		console.log();

		// calculcations
		var shirtProfit = shirtSellingPrice - shirtManufacturing;
		var hoodyProfit = hoodySellingPrice - hoodyManufacturing;
		var shirtProfitWithShipping = shirtProfit - shipping;
		var hoodyProfitWithShipping = hoodyProfit - shipping;

		/* ********************************************************** */
		/* de tekst een kleur geven bij hoge lage en gemiddelde winst */
		/* ********************************************************** */

		// CSS shirt profit
		let profitCssShirt;
		if ( shirtProfit == targetProfit ) {
				profitCssShirt = "blue";
		} else if ( shirtProfit > targetProfit ) {
				profitCssShirt = "green";
		} else {
				profitCssShirt = "red";
		}
		console.log("--- shirt profit");
		console.log("shirtProfit:", shirtProfit);
		console.log("profitCssShirt:", profitCssShirt);

		// shirt profit with shipping
		let profitCssShirtShipping;
		if ( shirtProfitWithShipping == targetProfit ) {
				profitCssShirtShipping = "blue";
		} else if ( shirtProfitWithShipping > targetProfit ) {
				profitCssShirtShipping = "green";
		} else {
				profitCssShirtShipping = "red";
		}
		console.log();
		console.log("--- shirt profit with shipping");
		console.log("shirtProfitWithShipping:", shirtProfitWithShipping);
		console.log("profitCssShirtShipping:", profitCssShirtShipping);

		// hoody profit
		let profitCssHoodie;
		if ( hoodyProfit == targetProfit ) {
				profitCssHoodie = "blue";
		} else if ( hoodyProfit > targetProfit ) {
				profitCssHoodie = "green";
		} else {
				profitCssHoodie = "red";
		}
		console.log();
		console.log("--- hoody profit");
		console.log("targetProfit:", targetProfit);
		console.log("hoodyProfit:", hoodyProfit);
		console.log("profitCssHoodie:", profitCssHoodie);

		// hoody profit with shipping
		let profitCssHoodieShipping;
		if ( hoodyProfitWithShipping == targetProfit ) {
				profitCssHoodieShipping = "blue";
		} else if ( hoodyProfitWithShipping > targetProfit ) {
				profitCssHoodieShipping = "green";
		} else {
				profitCssHoodieShipping = "red";
		}
		console.log();
		console.log("--- hoody profit with shipping");
		console.log("targetProfit:", targetProfit);
		console.log("hoodyProfitWithShipping:", hoodyProfitWithShipping);
		console.log("profitCssHoodieShipping:", profitCssHoodieShipping);

		// uitkomst tonen
		const outputDiv = document.getElementById('output'); // de de div zoeken
		console.log();
		console.log('outputDiv:', outputDiv); // kijk de div gevonden is
		outputDiv.innerHTML = `
			<ul>
				<li class="title">Shirt €` + shirtSellingPrice + `</li>
				<li class="resultLi ` + profitCssShirt + `"><b>€ ` + shirtProfit + ` </b><i>profit</i></li>
				<li class="resultLi ` + profitCssShirtShipping + `"><b>€ ` + shirtProfitWithShipping + ` </b><i>profit, <b>with shipping</b></i></li>

				<li class="newSection title">Hoody €` + hoodySellingPrice + `</li>
				<li class="resultLi ` + profitCssHoodie + `"><b>€ ` + hoodyProfit + ` </b><i>profit</i></li>
				<li class="resultLi ` + profitCssHoodieShipping + `"><b>€ ` + hoodyProfitWithShipping + ` </b><i>profit, <b>with shipping</b></i></li>
			</ul>
		`;

		// div zichtbaar maken
		outputDiv.classList.remove('hidden');
	});
});
