const CURRENCY_LOCALE = "en-US";

const CURRENCY_FORMAT_OPTIONS = {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
};

export function formatCurrency(value) {
    return Number(value).toLocaleString(CURRENCY_LOCALE, CURRENCY_FORMAT_OPTIONS);
}

export function formatCurrencyWithSymbol(value) {
    return `${formatCurrency(value)} €`;
}

const currencyTickCallback = (value) => formatCurrency(value);

const currencyTooltipLabelCallback = (context) => {
    const label = context.dataset.label ? `${context.dataset.label}: ` : "";
    const value = context.parsed.y ?? context.parsed;
    return `${label}${formatCurrency(value)} €`;
};

export const chartCurrencyTooltip = {
    callbacks: {
        label: currencyTooltipLabelCallback,
    },
};

export const chartCurrencyYAxis = {
    ticks: {
        callback: currencyTickCallback,
    },
};
