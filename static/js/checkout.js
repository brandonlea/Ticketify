// Update post code label based on country
const countrySelect = document.getElementById('country');
const postcodeLabel = document.getElementById('postcode-label');
const postcodeInput = document.getElementById('post_code');

function updatePostCodeLabel() {
    const country = countrySelect.value;

    if (country === 'United States') {
        postcodeLabel.textContent = 'ZIP Code *';
        postcodeInput.placeholder = 'Enter your ZIP code';
    } else if (country === 'Ireland') {
        postcodeLabel.textContent = 'Eircode *';
        postcodeInput.placeholder = 'Enter your Eircode';
    } else if (country === 'Canada') {
        postcodeLabel.textContent = 'Postal Code *';
        postcodeInput.placeholder = 'Enter your postal code';
    } else {
        postcodeLabel.textContent = 'Post Code *';
        postcodeInput.placeholder = 'Enter your post code';
    }
}

// Update label on page load
updatePostCodeLabel();

// Update label when country changes
countrySelect.addEventListener('change', updatePostCodeLabel);