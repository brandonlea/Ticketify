// Initialize Stripe (stripe and elements are set from template variables)
const stripe = Stripe(window.stripePublicKey);
const elements = stripe.elements();
const cardElement = elements.create('card', {
    hidePostalCode: true,
    style: {
        base: {
            fontSize: '16px',
            color: '#32325d',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    }
});

cardElement.mount('#card-element');

cardElement.on('change', function(event) {
    const displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

const form = document.getElementById('payment-form');
const submitButton = document.getElementById('submit-button');
const buttonText = document.getElementById('button-text');
const spinner = document.getElementById('spinner');

// Update post code label based on country
const countrySelect = document.getElementById('billing-country');
const postcodeLabel = document.getElementById('postcode-label');
const postcodeInput = document.getElementById('billing-postcode');

function updatePostCodeLabel() {
    const country = countrySelect.value;

    if (country === 'US') {
        postcodeLabel.textContent = 'ZIP Code *';
        postcodeInput.placeholder = 'Enter your ZIP code';
    } else if (country === 'IE') {
        postcodeLabel.textContent = 'Eircode *';
        postcodeInput.placeholder = 'Enter your Eircode';
    } else if (country === 'CA') {
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

form.addEventListener('submit', async function(event) {
    event.preventDefault();

    submitButton.disabled = true;
    buttonText.classList.add('hidden');
    spinner.classList.remove('hidden');

    // Get billing details
    const billingCountry = document.getElementById('billing-country').value;
    const billingPostcode = document.getElementById('billing-postcode').value;

    const {error, paymentIntent} = await stripe.confirmCardPayment(
        window.clientSecret,
        {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: window.orderDetails.fullName,
                    email: window.orderDetails.email,
                    address: {
                        line1: window.orderDetails.address,
                        city: window.orderDetails.city,
                        postal_code: billingPostcode,
                        country: billingCountry
                    }
                }
            }
        }
    );

    if (error) {
        const errorElement = document.getElementById('card-errors');
        errorElement.textContent = error.message;
        submitButton.disabled = false;
        buttonText.classList.remove('hidden');
        spinner.classList.add('hidden');
    } else {
        if (paymentIntent.status === 'succeeded') {
            window.location.href = window.paymentSuccessUrl;
        }
    }
});