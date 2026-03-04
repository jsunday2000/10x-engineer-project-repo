import Button from "./Button";

function Notification({ notification, onClose }) {
  if (!notification) {
    return null;
  }

  return (
    <div
      className={`notification notification-${notification.type}`}
      role="status"
      aria-live="polite"
    >
      <span>{notification.message}</span>
      <Button variant="ghost" size="sm" onClick={onClose}>
        Close
      </Button>
    </div>
  );
}

export default Notification;
