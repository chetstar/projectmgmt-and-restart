$(document).ready(function() {
            $(function() {
                $('#sortable').sortable({
                    start : function(event, ui) {
                        var start_pos = ui.item.index();
                        ui.item.data('start_pos', start_pos);
                    },
                    change : function(event, ui) {
                        var start_pos = ui.item.data('start_pos');
                        var index = ui.placeholder.index();
                    
                        
                        cIndex = (start_pos < index) ? index-2 : index-1;
                        ui.placeholder.prevAll('li').each(function(){
                            $this = $(this);
                            if($this.is(ui.item)) {return;}
                            $this.html(cIndex);
                            cIndex--;
                        });
                        
                        cIndex = (start_pos < index) ? index : index+1;
                        ui.placeholder.nextAll('li').each(function(){
                            $this = $(this);
                            if($this.is(ui.item)) return;
                            $this.html(cIndex)
                            cIndex++;
                        });
                        
                        ui.item.html((start_pos < index) ? index-1 : index);
                    },
                    axis : 'y'
                });
            });
};
