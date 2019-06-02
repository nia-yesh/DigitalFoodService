function myFunction() {
                let checkBox = document.getElementById("id_takeaway");
                let wprice = document.getElementById("with_price");
                let noprice = document.getElementById("without_price");

                let tot_wprice = document.getElementById("total_price_wt");
                let tot_noprice = document.getElementById("total_price_nt");

                if (checkBox.checked){
                    wprice.style.display = "inline";
                    noprice.style.display = "none";

                    tot_wprice.style.display = "inline";
                    tot_noprice.style.display = "none";
                } else {
                    noprice.style.display = "inline";
                    wprice.style.display = "none";

                    tot_noprice.style.display = "inline";
                    tot_wprice.style.display = "none";
                }
            }
            document.addEventListener('DOMContentLoaded', function() {
                var elems = document.querySelectorAll('.fixed-action-btn');
                var instances = M.FloatingActionButton.init(elems,'bottom');
              });
              $(document).ready(function() {
                $('.mdb-select').materialSelect();
                });