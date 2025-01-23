import React, { useState } from "react";
import "./CheckBox.css";

function CheckBox({ id, disabled }) {
  // 체크박스 상태 관리
  const [isChecked, setIsChecked] = useState(false);

  // 체크박스 상태 변경 처리
  const handleCheckboxChange = (event) => {
    setIsChecked(event.target.checked);
  };

  return (
    <div>
      <input
        type="checkbox"
        id={id}
        checked={isChecked}
        onChange={handleCheckboxChange}
        disabled={disabled} // 비활성화 상태 전달
      />
    </div>
  );
}

export default CheckBox;
