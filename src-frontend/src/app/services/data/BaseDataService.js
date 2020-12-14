import $ from 'jquery';

export default class BaseDataService {
  getJson(url) {
    return $.getJSON(url);
  }

  postJson(url, dataObj) {
    return $.ajax({
      url: url,
      type: 'POST',
      data: JSON.stringify(dataObj),
      contentType: 'application/json',
      dataType: 'json',
    });
  }
}
