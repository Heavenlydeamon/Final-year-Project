document.addEventListener("DOMContentLoaded", function() {
    var quizSelect = document.getElementById("id_quiz");
    var sectionSelect = document.getElementById("id_section_tag");

    function fetchSections(quizId) {
        if (!quizId) {
            sectionSelect.innerHTML = '<option value="">All sections</option>';
            return;
        }

        // Keep current selected value to re-apply it after fetching
        var currentValue = sectionSelect.value;
        
        fetch('/quiz/admin-sections/?quiz_id=' + quizId)
            .then(response => response.json())
            .then(data => {
                sectionSelect.innerHTML = '<option value="">All sections</option>';
                if (data.sections && Array.isArray(data.sections)) {
                    data.sections.forEach(function(sec) {
                        if (sec.id && sec.label) {
                            var option = document.createElement('option');
                            option.value = sec.id;
                            option.text = sec.label;
                            if (sec.id === currentValue) {
                                option.selected = true;
                            }
                            sectionSelect.appendChild(option);
                        }
                    });
                }
            })
            .catch(error => console.error('Error fetching sections:', error));
    }

    if (quizSelect && sectionSelect) {
        quizSelect.addEventListener("change", function() {
            fetchSections(this.value);
        });
        
        // Fetch initially if no options are present (e.g. creating new question but quiz is pre-selected)
        if (quizSelect.value && sectionSelect.options.length <= 1) {
            fetchSections(quizSelect.value);
        }
    }
});
