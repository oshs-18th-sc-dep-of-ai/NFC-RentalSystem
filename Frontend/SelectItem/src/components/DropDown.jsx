import React from "react";
import "./DropDown.css";

const DropDown = ({ visibility, children }) => {
  const [visibilityAnimation, setVisibilityAnimation] =
    React.useState(visibility);
  const timeoutRef = React.useRef(null);

  React.useEffect(() => {
    if (visibility) {
      clearTimeout(timeoutRef.current);
      setVisibilityAnimation(true);
      timeoutRef.current = null;
    } else {
      timeoutRef.current = setTimeout(() => {
        setVisibilityAnimation(false);
        timeoutRef.current = null;
      }, 400);
    }

    return () => {
      clearTimeout(timeoutRef.current);
    };
  }, [visibility]);

  return (
    <div
      className={`components-dropdown ${
        visibility ? "slide-fade-in-dropdown" : "slide-fade-out-dropdown"
      }`}
    >
      {visibilityAnimation && children}
    </div>
  );
};

const DropDownBox = ({ onChange }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [selectedOption, setSelectedOption] = React.useState("빌릴 물품");
  const dropdownRef = React.useRef(null);

  // Close the dropdown when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const toggleDropdown = () => {
    setIsOpen((prev) => !prev);
  };

  const handleOptionClick = (option) => {
    setSelectedOption(option);
    onChange(option); // 부모 컴포넌트로 선택된 값을 전달
    setIsOpen(false);
  };

  return (
    <div className="dropdown-box-container" ref={dropdownRef}>
      <button
        className="dropdown-toggle-button"
        onClick={toggleDropdown}
        aria-expanded={isOpen}
      >
        {selectedOption}
      </button>
      <DropDown visibility={isOpen}>
        <ul className="dropdown-options" role="menu">
          {["양심 우산", "양심 슬리퍼"].map((option) => (
            <li
              key={option}
              className="dropdown-option"
              role="menuitem"
              onClick={() => handleOptionClick(option)}
            >
              {option}
            </li>
          ))}
        </ul>
      </DropDown>
    </div>
  );
};

export default DropDownBox;
