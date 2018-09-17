
$("#plus_button").click(function add_choice() {
        var dishOption = `
                    <li>
                        <div class="card">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-4">
                                        <img class="img-thumbnail" src="https://d2mekbzx20fc11.cloudfront.net/uploads/Morroccan_Lamb_UC_500x333-rei2.png">
                                    </div>
                                    <div class="col-md-8">
                                        <div class="form-group">
                                            <label>Name of the dish</label>
                                            <input class="form-control" type="text" name="choiceList[]" value=""/>
                                        </div>
                                        <div class="form-group">
                                            <label>Description</label>
                                            <textarea class="form-control" type="text" name="choiceList[]" value=""></textarea>
                                        </div>
                                    </div>
                                </div>
                    
                            </div>
                        </div>
                        <br>
                    </li>
        `;
        $("#choices_container").append(dishOption);

    }
)
