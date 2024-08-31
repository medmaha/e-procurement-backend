try {
	app.unmount();
} catch (err) {
	let app = Vue.createApp({
		data: () => {
			return {
				loading: "",
				disabled: false,
				rfqNumber: "",
				reqNumber: "",
				staff_account: AUTH_USER?.profile,
				todaysDate: new Date().toISOString().split("T")[0],
			};
		},
		created() {
			document.addEventListener("DOMContentLoaded", () => {
				// const employerInput = document.getElementById("id_employer_name");
				// employerInput.value = this.authUser.name;
			});
		},
		methods: {
			submitRequisition() {
				this.loading = true;
				this.disabled = true;
			},
		},
		delimiters: ["[[", "]]"],
	}).mount("#requisitionContainer");
}
