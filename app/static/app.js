const { createApp } = Vue;

createApp({
  data() {
    return {
      html: "",
      prompt: "",
      extracted_data: {},
      emailText: "",
      filename: "",
      fromAddress: "",
      toAddress: "",
      receivedDate: ""
    };
  },
  methods: {
    async handleUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.filename = file.name;

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/upload", {
        method: "POST",
        body: formData
      });

      const result = await res.json();
      this.html = result.html;
      this.emailText = result.text;
      this.fromAddress = result.from || "";
      this.toAddress = result.to || "";
      this.receivedDate = result.date || "";
    },

    async handleExtract() {
      const res = await fetch("/extract", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: this.prompt,
          email_text: this.emailText,
          from: this.fromAddress,
          to: this.toAddress,
          date: this.receivedDate
        })
      });

      const result = await res.json();
      this.extracted_data = result.extracted_data || {};
    }
  }
}).mount("#app");
