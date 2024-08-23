// HOOKAH-LIST

// обработчик клика для всех карточек

document.querySelectorAll('.card').forEach(function(card) {
    card.addEventListener('click', function(event) {
        // Проверяем, что клик был не по кнопке "Избранное"
        if (!event.target.closest('.favorite-toggle') && !event.target.closest('.card-btn-hookah-list')) {
            window.location.href = this.getAttribute('data-href');
        }
    });
});

// выпадающий список вкусов табака

function toggleFlavorsField() {
    var categoryField = document.getElementById('id_category');
    var flavorsField = document.getElementById('flavors-field');
    var selectedCategory = categoryField.options[categoryField.selectedIndex].text;

    if (selectedCategory.includes('Табак')) {
        flavorsField.style.display = 'block';
    } else {
        flavorsField.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    toggleFlavorsField();
});

// лайки
