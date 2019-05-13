/* globals
$:false
Papa:false
dfjs:false
*/
const csvUrl = 'https://raw.githubusercontent.com/organizejs/collective-actions-in-tech/master/actions.csv'
var masterDf = null /* global */
var queryTags = []

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

  // setup event to toggle source links
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
        let options = { 
          weekday: 'long', 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric', 
          timeZone: 'UTC' 
        }
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

/**
 * Populated the HTML with a df
 * @param {df} dataframe 
 */
function populateHtml (df, query, showCount=false) {
  $('#actions').empty()

  // show number results if search
  if (df.count() === masterDf.count() && !showCount) {
    $('#action-count').hide()
  } else {
    count = (!query) ? 0 : df.count()
    $('#action-count').html("found: " + count).show()
  }

  // setup search cancel icon
  if (query) {
    $("#search-cancel-icon").click(function() {
      console.log("clicked")
    }).show()
  }

  // Add rows to html
  for (let i = 0; i < df.count(); i++) {
    let row = df.getRow(i).toDict()
    let html = rowToHtml(row)
    $('#actions').append(html)
  }

  // iterate through tags
  $(".tag").each(function() {
      if (query && query.includes($(this).html())) {
          // highlight if match
          $(this).addClass("selected")
      } else {
          // make tags clickable
          $(this).click(function() {
              tag = $(this).html()
              addQuery(tag)
          })
      }
  })
}

/**
 * Adds tag to the query-tags div
 * @param {str} of tag to add
 */
function addQuery (tag) {
  $("#query-cancel").show()
  let tagEl = $("<div>").addClass("query-tag").html(tag)
  $("#query-tags").append(tagEl)
  updateUrl()
}

/**
 * Update url
 **/
function updateUrl () {
  let tags = getQueryTags()
  if (tags.length > 0) {
    window.history.pushState({ foo: "bar" }, '', '/index?query=' + tags)
  } else {
    window.history.pushState({ foo: "bar" }, '', '/index')
  }
}

/**
 * Gets tags in query-tags div
 * @return {array} of tags
 */
function getQueryTags () {
  return $("#query-tags")
    .find(".query-tag")
    .map(function() {
      return $(this).html()
    })
    .get()
    .join(',')
}

/**
 * Clear queries
 */
function clearQueryTags () {
  $("#query-cancel").hide()
  $("#query-tags").empty()
  updateUrl()
}

/**
 * Create df from csv
 * @param {array} array of rows of the csv
 */
function createAndDisplayDf (data, callback) {
  let DataFrame = dfjs.DataFrame
  data.pop() // remove the last element, for some reason, papaparse loads an additional empty element
  masterDf = new DataFrame(data.slice(1), data[0])
  populateHtml(masterDf, null, false)
  callback()
}

/**
 * Searches through the df
 * @param {str} query string
 */
function includesAll(haystack, needles){ 
  for (let i = 0; i < needles.length; i++){
     if($.inArray(needles[i], haystack) == -1) return false;
  }
  return true;
}

/**
 * Searches through the df
 * @param {str} query string
 */
function search(query) {
  query = query.split(",")
  tmpDf = masterDf.where(row => query.every((val) => row.toArray().includes(val)))
  if (tmpDf.count() === 0) {
      populateHtml(masterDf, null, true)
  } else {
      populateHtml(tmpDf, query, true)
  }
}

// entry point
$(document).ready(function () {

  // load data
  parseData(csvUrl, function(data) {
    createAndDisplayDf(data, function() {

      // Add summary to html
      $('#action-total').append(masterDf.count())

      // on query list update
      $("#query-tags").on('DOMSubtreeModified', function() {
        let tags = getQueryTags()
        search(tags)
      })

      // clear query 
      $("#query-cancel").click(function() {
        clearQueryTags()
      })

      // check url for params
      let url = new URL(window.location)
      let query = url.searchParams.get("query")
      if (query) {
        query = query.split(',')
        for (let i = 0; i < query.length; i++) {
          addQuery(query[i])
        }
      }

      // on search
      $('#search-input').keypress(function(e){
        if(e.keyCode==13) {
          addQuery($(this).val())
          $(this).val("")
        }
      })
 
    })
  })
 
})
