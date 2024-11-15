import React from "react";

const DropDown = (props) => {
  const [visibilityAnimation, setVisibilityAnimation] = React.useState(false);
  const [repeat, setRepeat] = React.useState(null);
  React.useEffect(() => {
    {
      /* ← add */
    }
    if (props.visibility) {
      clearTimeout(repeat);
      setRepeat(null);
      setVisibilityAnimation(true);
    } else {
      setRepeat(
        setTimeout(() => {
          setVisibilityAnimation(false);
        }, 400)
      );
    }
  }, [props.visibility]);
  return (
    <article
      className={`components-dropdown ${
        props.visibility ? "slide-fade-in-dropdown" : "slide-fade-out-dropdown"
      }`}
    >
      {visibilityAnimation && props.children}
    </article>
  );
};

export default DropDown;
