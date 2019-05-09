/* globals
$:false
Papa:false
dfjs:false
*/
const csvUrl = 'https://raw.githubusercontent.com/organizejs/collective-actions-in-tech/master/actions.csv'

$(document).ready(function () {
  /*
    // inject readme from collective actions in tech repo to html body
    $.get(readmeRawUrl, function(data) {
        var converter = new showdown.Converter();
        var text = data;
        var html = converter.makeHtml(text);
        $("#content").append(html);
    })
  */

  /**
   * Gets the domain hostname from a url.
   * @param {str} the url
   * @return {str} domain hostname of the url
   */
  function urlDomain (url) {
    let a = document.createElement('a')
    a.href = url
    return a.hostname
  }

  /**
   * Creates a url elements to insert into the DOM.
   * @param {str} the url
   * @return {str} the html element
   */
  function createUrlEl (url) {
    return "<a href='" + url + "' taget='_blank'><span class='source'>" + urlDomain(url) + '</span></a>'
  }

  /**
   * Creates a tag elements to insert into the DOM.
   * @param {str} value of the tag
   * @return {str} the html element
   */
  function createTagEl (tag) {
    return "<span class='tag'>" + tag + '</span>'
  }

  /**
   * Uses Papaparse to parse csv file
   * @param {str} the url location of the csv to parse
   * @param {function} the callback that will consume the parsed csv
   */
  function parseData (url, callback) {
    Papa.parse(url, {
      download: true,
      dynamicTyping: true,
      complete: function (results) {
        callback(results.data)
      }
    })
  }

  /**
   * Gets all elements that contain the class 'sources' except for the one that is pass into the function as a param
   * @param {JqueryElement} The jquery element to exclude
   * @return {[HtmlElement]} A list of the html elements
   */
  function getAllSourceElementsExcept (sourcesEl) {
    let els = $('body').find('.sources')
    let ret = []
    for (let i = 0; i < els.length; i++) {
      if (!sourcesEl.is(els[i])) {
        ret.push(els[i])
      }
    }
    return ret
  }

  /**
   * Converts a DataFrame row into an html element that can be added to the DOM
   * @param {DataFrame Row} The dataframe row
   * @return {HtmlElement} Html element to add
   */
  function rowToHtml (row) {
    let action = $("<div class='action'></div>")
    let date = $("<div class='date'></div>")
    let tags = $("<div class='tags'></div>")
    let description = $("<div class='description'></div>")
    let sources = $("<div class='sources'></div>")
    let sourceIcon = $("<div class='source-icon'><i class='fas fa-link'></i></div>")

    sourceIcon.click(function () {
      let otherSources = getAllSourceElementsExcept(sources)
      for (let i = 0; i < otherSources.length; i++) {
        $(otherSources[i]).hide()
      }

      if (sources.is(':visible')) {
        sources.hide()
      } else {
        sources.show()
      }
    })

    for (let key in row) {
      let val = row[key]
      switch (key) {
        case 'null':
          break
        case 'date':
          let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
          let dateStr = new Date(val).toLocaleDateString('en-US', options)
          date.html(dateStr)
          break
        case 'description':
          description.html(val)
          break
        case 'sources':
          let urls = val.split(',')
          for (let i = 0; i < urls.length; i++) {
            sources.append(createUrlEl(urls[i]))
          }
          break
        case 'workers':
          break
        case 'author':
          break
        default:
          if (val) {
            let vals = val.split(',')
            for (let i = 0; i < vals.length; i++) {
              if (vals[i] !== 'None') {
                tags.append(createTagEl(vals[i]))
              }
            }
          }
          break
      }
    }

    action.append(date)
    action.append(description)
    action.append(sources)
    action.append(sourceIcon)
    action.append(tags)
    return action
  }

  parseData(csvUrl, function (data) {
    var DataFrame = dfjs.DataFrame
    let df = new DataFrame(data.slice(1), data[0])

    // Add summary to html
    $('#content #action-count').append(df.count())

    // Add rows to html
    for (let i = 0; i < df.count() - 1; i++) {
      let row = df.getRow(i).toDict()
      let html = rowToHtml(row)
      $('#content').append(html)
    }
  })
})
