

    function increment() {
        var qtyInput = document.getElementById("qty");
        var currentValue = parseInt(qtyInput.value);
        qtyInput.value = currentValue + 1;

    }

    function decrement() {
        var qtyInput = document.getElementById("qty");
        var currentValue = parseInt(qtyInput.value);
        var minvalue = parseInt(qtyInput.min);
        if (currentValue > minvalue) {
            qtyInput.value = currentValue - 1;
        }
    }

    function cart(csrf) {
        var qty = document.getElementById("qty");
        var pid = document.getElementById("pid");
        var qty = parseInt(qty.value);
        if (qty > 0) {
            let postObj = {
                product_qty: qty,
                pid: pid.value,
            }
            fetch("/addtocart",{
                method:"POST",
                credentials:"same-origin",
                headers:{
                    'Accept':"application/json",
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken':csrf,
                },
                body: JSON.stringify(postObj)
            }).then(response =>{
                return response.json();
            }).then(data =>{
                //console.log(data);
                alert(data['status']);
            })
        }
    }

    function fav(csrf) {
        var pid = document.getElementById("pid");
        let postObj={
            'pid':pid.value
        }
            fetch("/fav",{
                method:"POST",
                credentials:"same-origin",
                headers:{
                    'Accept':"application/json",
                    'X-Requested-With':'XMLHttpRequest',
                    'x-CSRFToken':csrf,
                },
                body: JSON.stringify(postObj)
            }).then(response =>{
                return response.json();
            }).then(data =>{
                alert(data['status']);
            })
    }