try {
	app.unmount();
} catch (err) {
	let app = Vue.createApp({
		data: () => {
			return {
				authUser: AUTH_USER,
				rfqNumber: "",
				rfqItems: [],
				generating: false,
				formData: { rfq: {}, rfqItems: {} },
			};
		},
		created() {
			document.addEventListener("DOMContentLoaded", () => {
				const employerInput = document.getElementById("id_employer_name");
				employerInput.value = this.authUser.name;
			});
		},
		methods: {
			promptRFQNumberGeneration(event) {
				event.preventDefault();
				const form = event.target.closest("form");
				if (form.checkValidity()) {
					const json = Object.fromEntries(new FormData(form).entries());
					this.formData["rfq"] = { ...json, rfq_number: this.rfqNumber };
					this.openRFQNumberDialog();
				} else form.reportValidity();
			},
			toggleRfqScaling(event) {
				const button = event.currentTarget;
				button.firstChild.classList.toggle("rotate-180");

				this.$refs.rfq.classList.toggle("opacity-0");
				this.$refs.rfq.classList.toggle("scale-y-0");
				this.$refs.rfq.classList.toggle("p-6");
				this.$refs.rfq.classList.toggle("h-0");
			},
			openRFQNumberDialog() {
				this.$refs.rfqNumberDialog.showModal();
			},
			closeRFQNumberDialog() {
				this.$refs.rfqNumberDialog.close();
			},
			generateRFQNumber() {
				this.rfqNumber = getFQToken(5);
				this.$refs.genRFQBnt.setAttribute("disabled", "true");
				this.closeRFQNumberDialog();
			},
		},
		delimiters: ["[[", "]]"],
	}).mount("#rfqContainer");
}

function getFQToken(size = 8) {
	const hex = "0123456789";
	let output = "";
	for (let i = 0; i < size - 3; i++) {
		let index = Math.floor(Math.random() * hex.length);
		output += hex.charAt(index);
	}
	return "RFQ" + output;
}
