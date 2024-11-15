import "./content.css";
import Dropdown from "./DropDown";
import { useState } from "react";

const Content = (props) => {
  const [dropdownVisibility, setDropdownVisibility] = useState(false);
  return (
    <>
      <div id="itemSelect">
        <button onClick={(e) => setDropdownVisibility(!dropdownVisibility)}>
          물품선택
        </button>
        <Dropdown visibility={dropdownVisibility}>
          <ul>
            <li>양심 우산</li>
            <li>양심 슬리퍼</li>
          </ul>
        </Dropdown>
      </div>
    </>
  );
};
export default Content;
