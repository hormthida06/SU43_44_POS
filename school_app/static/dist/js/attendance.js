document.querySelectorAll('.status-radio').forEach(radio => {
  radio.addEventListener('change', function() {
    const attendanceId = this.dataset.id;
    const status = this.value;

    fetch("{% url 'update_status' %}", {
      method: "POST",
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `attendance_id=${attendanceId}&status=${status}`
    })
    .then(res => res.json())
    .then(data => {
      if (!data.success) {
        alert("Error updating status!");
      }
    });
  });
});