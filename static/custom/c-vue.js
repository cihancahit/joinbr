Vue.component("paginated-list",{data:()=>({pageNumber:1,size:2,filtere:"*"}),props:{listData:{type:Array,required:!0},listData2:{type:Array,required:!1}},methods:{nextPage(){this.pageNumber++},prevPage(){this.pageNumber--},changeItem(){console.log(this.size)},filteredData(){return this.listData.filter(e=>"*"==this.filtere||this.filtere===e.event.ticket_type)},FilterEvent:function(e){return"*"==this.filtere||this.filtere===e}},computed:{pageCount(){let e=this.filteredData().length,t=this.size;return Math.ceil(e/t)},paginatedData(){let e=0;const t=(e=1==this.pageNumber?0:(this.pageNumber-1)*this.size)+parseInt(this.size);return new_list=this.filteredData(),new_list.slice(e,t)}},template:'\n    <div class="row exd-e-past">\n            <div class="col-12 exd-panel-h-con">\n                <h5 class="exd-panel-title">Past Events</h5>\n                <div>\n                    <select name="changepn" class="form-control" id="exdeventfilter" v-model="filtere">\n                        <option value="*">All Events Type</option>\n                        <option value="paid">Paid</option>\n                        <option value="free">Free</option>\n                        <option value="donation">Donation</option>\n                    </select>\n                </div>\n            </div>\n    \n            <div class="col-12 event-row py-3" v-for="event in paginatedData">\n        \n                <div class="row" v-show="FilterEvent(event.event.ticket_type)">\n                    <div class="col-md-4">\n                        <div class="img-con">\n                            <a v-bind:href="event.event.slug">\n                                <img v-bind:src="event.event.event_img" alt="" class="exd-e-past-event-image">\n                            </a>\n                            \n                            <div v-if="event.tag.tags === \'Organizer\'"class="event-label-organizer">\n                                <p>{{event.tag.tags}}</p>\n                            </div>\n                            <div v-if="event.tag.tags === \'Speaker\'"class="event-label-speaker">\n                                <p>{{event.tag.tags}}</p>\n                            </div>\n                            <div v-if="event.tag.tags === \'Atendee\'"class="event-label-atendee">\n                                <p>{{event.tag.tags}}</p>\n                            </div>\n                        </div>\n                    </div>\n                    <div class="col-md-8">\n                        <div class="exd-e-event-meta">\n                            <a v-bind:href="event.event.slug" class="title">{{ event.event.name }}</a>\n                            <a v-bind:href="event.event.slug" class="see-detail">see event\n                                                            details</a>\n                        </div>\n                        <div>\n                            <p>{{ event.event.info }}...</p>\n                        </div>\n                    </div>\n                </div>\n            </div>\n            <div class="pagination-bottom col-12 py-3">\n                <div class="pag-info">\n                    <p>Displaying <span>{{ this.paginatedData.length }}</span> - {{this.listData.length}} results </p>\n                </div>\n                <div class="pag-paginate">\n                    <p v-if="pageNumber === 1">Previous</p>\n                    <a v-else @click="prevPage">Prevous</a>\n                    <a v-if="pageNumber > 1" @click="prevPage">{{pageNumber-1}}</a>\n                    <a class="page-active">{{pageNumber}}</a>\n        \n                    <a v-if="pageNumber <= pageCount -1" @click="nextPage">{{pageNumber+1}}</a>\n                    <a v-if="pageNumber <= pageCount -1" @click="nextPage">Next</a>\n                    <p v-else>Next</p>\n                </div>\n            </div>\n    </div>\n  '}),new Vue({el:"#events-container",data:{events:[]},mounted:function(){this.getEvents()},methods:{getEvents:function(){this.loading=!0;var e=window.location.pathname.split("/")[2];this.$http.get("/experts/api/experts/past_events/"+e).then(e=>{this.events=e.data}).catch(e=>{console.log(e)})}}});