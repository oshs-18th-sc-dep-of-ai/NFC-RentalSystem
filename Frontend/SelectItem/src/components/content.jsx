import { useState } from "react";
import "./content.css";
import DropDownBox from "./DropDown";
import CheckBox from "./CheckBox";

const Content = () => {
  const [dropdownValue, setDropdownValue] = useState(null); // 드롭다운에서 선택된 값을 상태로 관리
  const [disabledCheckboxes, setDisabledCheckboxes] = useState([]); // 비활성화된 체크박스를 추적

  // 드롭다운 값이 변경될 때마다 호출되는 함수
  const handleDropdownChange = (value) => {
    const options = ["양심 우산", "양심 슬리퍼"];
    const index = options.indexOf(value); // 선택된 옵션에 맞는 인덱스 찾기
    setDropdownValue(index); // 선택된 값을 상태에 저장
  };

  // 체크박스를 선택하고 제출 버튼을 눌렀을 때 처리
  const handleSubmit = () => {
    // 비활성화할 체크박스 번호 추출
    const disabled = [];
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    checkboxes.forEach((checkbox, index) => {
      if (checkbox.checked) {
        disabled.push(index);
      }
    });
    setDisabledCheckboxes(disabled); // 비활성화된 체크박스 번호 상태로 저장
  };

  return (
    <>
      <div id="itemSelect">
        <DropDownBox onChange={handleDropdownChange} />{" "}
        {/* onChange로 부모에게 값 전달 */}
      </div>
      {/* 드롭다운 값이 선택되었을 때 체크박스를 렌더링 */}
      {dropdownValue !== null && (
        <div id="checkbox-container">
          {renderCheckboxes(dropdownValue, disabledCheckboxes)}{" "}
          {/* 선택된 값에 맞는 체크박스들 렌더링 */}
        </div>
      )}
      <button onClick={handleSubmit}>빌리기</button> {/* 제출 버튼 */}
    </>
  );
};

export default Content;

// 체크박스 생성 함수
const renderCheckboxes = (dropdownValue, disabledCheckboxes) => {
  const name = ["☂️", "🩴"]; // 선택된 값에 맞춰서 사용할 아이콘 배열
  const checkboxes = [];

  // 10개의 체크박스를 생성
  for (let i = 0; i < 10; i++) {
    checkboxes.push(
      <div key={i} className="checkbox-item">
        <div className="icon-container">
          <span className="checkbox-icon">{name[dropdownValue]}</span>{" "}
          {/* 아이콘을 위에 올림 */}
        </div>
        <CheckBox
          id={`checkbox${i}`}
          disabled={disabledCheckboxes.includes(i)} // 체크박스가 비활성화되어야 할지 여부를 확인
        />
        <label htmlFor={`checkbox${i}`}>{i + 1}</label> {/* 번호만 출력 */}
      </div>
    );
  }
  return checkboxes; // 체크박스들 반환
};
