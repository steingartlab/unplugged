function compareObjects(obj1, obj2) {
    // Get the keys of the objects
    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    // If the objects have a different number of keys, they are not equal
    if (keys1.length !== keys2.length) {
        return false;
    }

    // Compare the values of each key in the objects
    for (const key of keys1) {
        if (obj1[key] !== obj2[key]) {
            return false;
        }
    }

    // If all keys and values are equal, the objects are equal
    return true;
};

function commit(META) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/commit');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert('Commit successful!');
        } else {
            alert('Commit failed!');
        }
    };
    const data = {};
    for (const [jig, incumbentJigData] of Object.entries(META)) {
        const row = document.querySelector(`[name="${jig}_status"]`).closest('tr');
        const status = row.querySelector('[name$="_status"]').value;
        const user = row.querySelector('[name$="_user"]').value;
        const exp_id = row.querySelector('[name$="_exp_id"]').value;
        const delay = row.querySelector('[name$="_delay"]').value;
        const duration = row.querySelector('[name$="_duration"]').value;
        const voltage_range = row.querySelector('[name$="_voltage_range"]').value;
        const gain_dB = row.querySelector('[name$="_gain_dB"]').value;
        const avg_num = row.querySelector('[name$="_avg_num"]').value;
        const mux_row = row.querySelector('[name$="_mux_row"]').value;
        updatedJigData = {
            'status': status,
            'user': user,
            'exp_id': exp_id,
            'delay': delay,
            'duration': duration,
            'voltage_range': voltage_range,
            'gain_dB': gain_dB,
            'avg_num': avg_num,
            'mux_row': mux_row,
        };

        is_identical = compareObjects(updatedJigData, incumbentJigData);
        console.log(is_identical);
        if (!is_identical) {
            data[jig] = updatedJigData;
        }
    }
    xhr.send(JSON.stringify(data));
};