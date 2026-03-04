function Button({
  variant = "primary",
  size = "md",
  type = "button",
  isLoading = false,
  disabled = false,
  className = "",
  children,
  ...props
}) {
  const combinedClassName = `btn btn-${variant} btn-${size} ${className}`.trim();

  return (
    <button
      type={type}
      className={combinedClassName}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <span className="btn-spinner" aria-hidden="true" /> : null}
      <span>{children}</span>
    </button>
  );
}

export default Button;
