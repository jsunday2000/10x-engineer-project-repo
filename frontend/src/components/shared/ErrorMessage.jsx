import Button from "./Button";

function ErrorMessage({ message, onDismiss }) {
  if (!message) {
    return null;
  }

  return (
    <div className="error-banner" role="alert">
      <span>{message}</span>
      <Button variant="ghost" size="sm" onClick={onDismiss}>
        Dismiss
      </Button>
    </div>
  );
}

export default ErrorMessage;
