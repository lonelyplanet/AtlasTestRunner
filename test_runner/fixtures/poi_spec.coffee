describe "poi", ->
  beforeEach ->
    @poi = Fixtures.Poi.make {
      name: "Jonathan Apple"
      type: "Eat"
      review: {
        detail: '<p>the details</p>'
        summary: '<p>the summary</p>'
      }
      place: {
        "@about": "http://atlas.devint.lpo/places/362813"
        "name": "Melbourne"
        "irrelevant": "data"
        "id": 362813
      }
      properties: [{key: 'attributes', value: 'wifi'}, {key: 'attributes', value: 'aircon'}]
    }

  describe '#new', ->

    beforeEach ->
      spyOn(window, 'Guid').andReturn('1234-5678')

    describe 'when created locally', ->

      beforeEach ->
        @newPoi = new DSC.models.Poi()

      it 'assigns the GUID to the ID', ->
        expect(@newPoi.id).toEqual('c1234-5678')

      it 'assigns the GUID to the CID', ->
        expect(@newPoi.cid).toEqual('c1234-5678')

      it 'assigns the URL to the @about attribute', ->
        expect(@newPoi.get('@about')).toEqual('/pois/c1234-5678/lang/en')

    describe 'when retrieved from server', ->
      beforeEach ->
        @existingPoi = new DSC.models.Poi(id: @poi.id)

      it 'does not create a GUID', ->
        expect(window.Guid).not.toHaveBeenCalled()

      it 'has the passed-in ID', ->
        expect(@existingPoi.id).toEqual(@poi.id)

  describe "Setting place data", ->
    it "ignores irrelevant data", ->
      expect(@poi.get('place').irrelevant).toBeUndefined()

  describe "hasNotes", ->
    describe "when notes is ''", ->
      beforeEach -> @poi.set(notes: '')
      it "is false", -> expect(@poi.hasNotes()).toBeFalsy()
    describe "when notes is null", ->
      beforeEach -> @poi.set(notes: null)
      it "is false", -> expect(@poi.hasNotes()).toBeFalsy()
    describe "when notes is 'the notes'", ->
      beforeEach -> @poi.set(notes: 'the notes')
      it "is truthy", -> expect(@poi.hasNotes()).toBeTruthy()

  it "knows place_id", ->
    expect(@poi.placeId()).toEqual(362813)

  describe "when the poi has a place", ->
    it "knows the place name", ->
      expect(@poi.placeName()).toEqual('Melbourne')

  describe "when the poi does not have a place", ->
    beforeEach ->
      @poi.set(place: null)

    it "raises an exception when the place name is checked", ->
      expect((=> @poi.placeName())).toThrow('POIs must be in a place')

  it "tour() is false", ->
    expect(@poi.tour()).toEqual(false)

  it "course() is false", ->
    expect(@poi.course()).toEqual(false)

  it "can modify telephones", ->
    @poi.set(telephones: [{text: "home"}])
    expect(@poi.get('telephones')[0].text()).toEqual "home"

  describe 'has course property', ->
    beforeEach ->
      @poi.set(properties:[{key:'attributes', value:'course'}])

    it "course() is true", ->
      expect(@poi.course()).toEqual(true)

  describe 'has tour property', ->
    beforeEach ->
      @poi.set(properties:[{key:'attributes', value:'tour'}])

    it "tour() is true", ->
      expect(@poi.tour()).toEqual(true)

  it 'toggles price range', ->
    expect(@poi.priceRangeString()).toEqual("N/A")
    @poi.togglePriceRange()
    expect(@poi.priceRangeString()).toEqual("Free")
    @poi.togglePriceRange()
    expect(@poi.priceRangeString()).toEqual("$")
    @poi.togglePriceRange()
    expect(@poi.priceRangeString()).toEqual("$$")
    @poi.togglePriceRange()
    expect(@poi.priceRangeString()).toEqual("$$$")
    @poi.togglePriceRange()
    expect(@poi.priceRangeString()).toEqual("N/A")

  describe "managing properties", ->
    beforeEach ->
      @changePropertiesSpy = jasmine.createSpy('changeProperties')
      @poi.bind('change:properties', @changePropertiesSpy)

    describe 'adding properties', ->
      beforeEach ->
        @poi.addProperty("jon", true)

      it "adds properties", ->
        expect(@poi.hasProperty("jon")).toEqual(true)

      it "triggers an event", ->
        expect(@changePropertiesSpy.argsForCall.length).toEqual 1
        expect(@changePropertiesSpy).toHaveBeenCalled()

    describe "removing properties", ->
      beforeEach ->
        @poi.addProperty("jon", true)
        @poi.addProperty("beer", true)
        @changePropertiesSpy.reset()
        @poi.removeProperty("jon")

      it "only removes the selected property", ->
        expect(@poi.hasProperty("jon")).toEqual(false)
        expect(@poi.hasProperty("beer")).toEqual(true)

      it 'triggers events for each addition and removal', ->
        expect(@changePropertiesSpy).toHaveBeenCalled()

    describe "manages attribute properties", ->
      it "removes multiple instances of a property", ->
        @poi.addProperty('attributes', 'swimmingpool')
        @poi.addProperty('attributes', 'swimmingpool')
        @poi.removeProperty("attributes", "swimmingpool")
        expect(@poi.hasProperty("attributes", "swimmingpool")).toEqual(false)

      describe "removing a property", ->
        beforeEach ->
          @poi.addProperty("attributes", "foobar")
          @poi.addProperty('attributes', 'swimmingpool')
          @poi.removeProperty('attributes', 'swimmingpool')
        it "removes the selected property", ->
          expect(@poi.hasProperty('attributes', 'swimmingpool')).toBeFalsy()

        it "does not remove other properties", ->
          expect(@poi.hasProperty('attributes', 'foobar')).toBeTruthy()

  describe "filtering", ->
    beforeEach ->
      @filter = new DSC.models.PoiFilter type: '', term: ''

    describe 'when search term is present', ->
      describe 'matches on type and term', ->
        beforeEach ->
          @filter.set({ type: 'Eat', term: 'term' })

        it 'fails if poi doesnt match type', ->
          @poi.set({ type: 'See', name: 'term' })
          expect(@poi.matchesFilter(@filter)).toBeFalsy()

        it 'fails if poi doesnt match term', ->
          @poi.set({ type: 'Eat', name: 'blah' })
          expect(@poi.matchesFilter(@filter)).toBeFalsy()

        it 'succeeds if poi matches both type and name', ->
          @poi.set({ type: 'Eat', name: 'term' })
          expect(@poi.matchesFilter(@filter)).toBeTruthy()

        it 'succeeds if poi matches both type and subtype', ->
          @poi.set({ type: 'Eat', name: 'agrajag', subtype: 'term' })
          expect(@poi.matchesFilter(@filter)).toBeTruthy()

    describe 'when search term is not present', ->
      describe 'matches on type and place', ->
        beforeEach ->
          @filter.set({ type: 'Eat', term: '' })

        it 'fails if poi doesnt match type', ->
          @poi.set({ type: 'See' })
          expect(@poi.matchesFilter(@filter)).toBeFalsy()

        it 'succeeds if poi matches type', ->
          @poi.set({ type: 'Eat' })
          expect(@poi.matchesFilter(@filter)).toBeTruthy()

  describe 'serializing', ->

    describe 'only sending the fields which have changed (differenceFromServer)', ->
      describe 'when a field changes from null to empty string', ->
        it 'is not treated as different', ->
          @poi.set hours: null
          @poi.resetAttrsAccordingToServer()
          @poi.set hours: ''
          expect(_.keys(@poi.differenceFromServer())).toEqual [ 'id' ]

      describe 'when a field changes from null to zero', ->
        it 'is treated as different', ->
          @poi.set price_range: null
          @poi.resetAttrsAccordingToServer()
          @poi.set price_range: 0
          expect(_.keys(@poi.differenceFromServer())).toEqual [ 'id', 'price_range' ]

      describe 'when the review summary has changed', ->
        beforeEach ->
          @poi.get('review').summary = '<p>fff</p>'
          @json = @poi.differenceFromServer()

        it 'does not serialize the name', ->
          expect(@json.name).toBeFalsy()

        it 'serializes the review summary', ->
          expect(@json.review.summary).toEqual('<p>fff</p>')

        it 'serializes the review detail', ->
          expect(@json.review.detail).toEqual('<p>the details</p>')

        it 'only serializes the changed fields', ->
          expect(_.keys(@json)).toEqual [ 'id', 'review' ]

        it 'can be serialized again', ->
          @json = @poi.differenceFromServer()
          expect(_.keys(@json)).toEqual [ 'id', 'review' ]

    describe 'toFullJSON', ->
      beforeEach ->
        spyOn(@poi, 'cleanReviews')

      it "has a root 'poi' element", ->
        expect(@poi.toFullJSON()['poi']).toBeDefined()

      it "never adds null to poi reviews", ->
        @poi.set({ review: { summary: null, detail: null } })
        json = @poi.toFullJSON()
        expect(json['poi']['review']['summary']).not.toEqual "null"
        expect(json['poi']['review']['detail']).not.toEqual "null"

      it "does not have events for address", ->
        poi = Fixtures.Poi.make()
        json = poi.toFullJSON().poi
        expect(json.address._callbacks).toBeUndefined()

      describe 'with unsaved changes', ->
        beforeEach ->
          @poi.unsavedChanges = -> true
          @poi.toFullJSON()

        it "cleans the reviews", ->
          expect(@poi.cleanReviews).toHaveBeenCalledOnce()

      describe 'with no unsaved changes', ->
        beforeEach ->
          @poi.toFullJSON()

        it "does not clean the reviews", ->
          expect(@poi.cleanReviews).not.toHaveBeenCalled()

      describe 'attrs according to server', ->

        describe 'model requires sync', ->
          beforeEach ->
            @poi.state.set(requiresSync: true)
            @json = @poi.toFullJSON()

          it 'should be defined', ->
            expect(@json.poi._attrsAccordingToServer).not.toBeUndefined()

        describe 'model does not requires sync', ->
          beforeEach ->
            @poi.state.set(requiresSync: false)
            @json = @poi.toFullJSON()

          it 'should not be defined', ->
            expect(@json.poi._attrsAccordingToServer).toBeUndefined()

  describe 'detecting unsaved changes', ->
    describe 'with no actual changes', ->
      beforeEach ->
        @poi.set(name: @poi.get('name'))

      it 'detects no changes', ->
        expect(@poi.unsavedChanges()).toBeFalsy()
        expect(@poi.requiresSync()).toBeFalsy()

      it 'always indicates unsaved changes if object has a cid (because it has not been saved)', ->
        @poi.set(id: 'c43')
        expect(@poi.unsavedChanges()).toBeTruthy()
        expect(@poi.requiresSync()).toBeTruthy()

    describe 'with unsaved changes to its properties', ->

      describe 'when properties are added', ->
        beforeEach ->
          @poi.addProperty('attributes', 'japanesemenu')

        it "detects changes", ->
          expect(@poi.unsavedChanges()).toBeTruthy()
          expect(@poi.requiresSync()).toBeTruthy()

      describe 'when properties are modified', ->
        beforeEach ->
          @poi.set(
            {
              name: 'AwesomePlace'
              address: {
                "street": 'Noob crescent'
              }
            }
          )
          @poi.set(unsavedChanges:false)
          @poi.set(requiresSync:false)
          @poi.set(
            {
              name: 'AwesomePlace'
              address: {
                "street": 'Legends court'
              }
            }
          )

        it "detects changes", ->
          expect(@poi.unsavedChanges()).toBeTruthy()
          expect(@poi.requiresSync()).toBeTruthy()

      describe "when properties are removed", ->
        beforeEach ->
          @poi.set(unsavedChanges:false)
          @poi.set(requiresSync:false)
          @poi.removeProperty('attributes', 'wifi')

        it "detects changes", ->
          expect(@poi.unsavedChanges()).toBeTruthy()
          expect(@poi.requiresSync()).toBeTruthy()

    describe 'with unsaved changes to the name', ->
      beforeEach ->
        @poi.set(name : "FooBoo")

      it 'detects changes', ->
        expect(@poi.unsavedChanges()).toBeTruthy()
        expect(@poi.requiresSync()).toBeTruthy()

  describe "#hasLatLng", ->
    it "is true when both lat and long are floats", ->
      @poi.set({ latitude: 1.0, longitude: 1.0 })
      expect(@poi.hasLatLng()).toBe true

    it "is false when one is not a float", ->
      @poi.set({ latitude: "", longitude: 1.0 })
      expect(@poi.hasLatLng()).toBe false

    it "is false for empty strings", ->
      @poi.set({ latitude: "", longitude: "" })
      expect(@poi.hasLatLng()).toBe false

    it "is false for null", ->
      @poi.set({ latitude: null, longitude: null })
      expect(@poi.hasLatLng()).toBe false

  describe "onSaveSuccess", ->
    beforeEach ->
      @poi.set('name': 'new name') # Have some unsaved changes, first
      spyOn(@poi, 'set').andCallThrough()
      @poi.onSaveSuccess(@poi,{id: '452524', place: "@about": '/places/52341'})

    it "updates the POI attrs", ->
      expect(@poi.set).toHaveBeenCalledWith({ id : '452524', place : { "@about" : '/places/52341', id : '52341' }})

    it "does not have save errors", ->
      expect(@poi.state.get('hasSaveErrors')).toBeFalsy()

    it "does not have any changed non-preserved fields", ->
      expect(_.keys @poi.differenceFromServer()).toEqual [ 'id' ]

  describe "onSaveError", ->
    beforeEach ->
      window.Airbrake = onSaveError: jasmine.createSpy('airbrake')
      spyOn(@poi, 'set')
      spyOn(DSC, 'trigger')
      @errorMsg = 'rawr - I am an error'
      spyOn(@poi, '_extractErrorsFromXmlResponse').andReturn([@errorMsg])
      @poi.onSaveError(@poi,@errorMsg)

    it "does not updates the POI attrs", ->
      expect(@poi.set).not.toHaveBeenCalled()

    it "updates the state", ->
      expect(@poi.state.get('hasSaveErrors')).toBeTruthy()
      expect(@poi.state.get('unsavedChanges')).toBeTruthy()
      expect(@poi.state.get('requiresSync')).toBeTruthy()

    it "triggers a CONTENT_SAVE_ERROR with the message", ->
      expect(DSC.trigger).toHaveBeenCalledWith(DSC.events.CONTENT_SAVE_ERROR, ["POI Jonathan Apple (#{@poi.get('id')}): rawr - I am an error", @poi])

    it "informs airbrake", ->
      expect(Airbrake.onSaveError).toHaveBeenCalledWith(@poi, @errorMsg)

  describe "Extracting errors from the xml response", ->
    beforeEach ->
      response = '<?xml version="1.0" ?><poi><name error="cant be blank"><review error="summary: Did not expect element strong there"></poi>'
      @returnedErrors = @poi._extractErrorsFromXmlResponse(response)

    it "returns both errors and details", ->
      expect(@returnedErrors).toEqual(['Name cant be blank', 'Review summary: Did not expect element strong there'])

  describe "#set", ->
    beforeEach ->
      @poi.set()

    it "sets the poi searchable name to its name when one is not defined", ->
      expect(@poi.get('searchable_name')).toEqual('jonathan apple')

    describe "when the searchable_name is set", ->
      beforeEach ->
        delete @poi.attributes.searchable_name
        @poi.set(searchable_name: 'jonathan likes apples')

      it "does not get changed", ->
        expect(@poi.get('searchable_name')).toEqual('jonathan likes apples')

  describe '#saving', ->

    describe 'unsuccessfully', ->
      beforeEach ->
        spyOn($, 'ajax')
        @poi.state.set(unsavedChanges: true)
        @poi.state.set(requiresSync:true)
        @poi.set(saveErrors: true)
        window.Airbrake = onSaveError: jasmine.createSpy('airbrake')
        $.ajax.andCallFake (options) ->
          options.error(responseXML: "error")
        @poi.save()
        waitsFor -> $.ajax.wasCalled

      it 'sets unsaved changes to true', ->
        expect(@poi.state.get('unsavedChanges')).toBeTruthy()

      it 'sets requiresSync to true', ->
        expect(@poi.state.get('requiresSync')).toBeTruthy()

      it 'sets saveErrors to true', ->
        expect(@poi.hasSaveErrors()).toBeTruthy()

      it "informs airbrake", ->
        expect(Airbrake.onSaveError).toHaveBeenCalledWith(@poi, responseXML: "error")

    describe 'successfully', ->
      beforeEach ->
        spyOn($, 'ajax').andCallFake (options) -> options.success()
        @poi.state.set(unsavedChanges: true)
        @poi.state.set(requiresSync:true)
        @poi.set(saveErrors: true)
        $.ajax.andCallFake (options) ->
          options.success()
        @poi.save()

      it 'sets unsaved changes to false', ->
        expect(@poi.state.get('unsavedChanges')).toBeFalsy()

      it 'sets requiresSync to false', ->
        expect(@poi.state.get('requiresSync')).toBeFalsy()

      it 'sets saveErrors to false', ->
        expect(@poi.hasSaveErrors()).toBeFalsy()

  describe 'validating content', ->

    describe 'with no review', ->

      beforeEach ->
        @poi.attributes.review = null

      it 'is valid', ->
        expect(@poi.validateContent()).toBeTruthy()

    describe 'with invalid ACML', ->

      beforeEach ->
        @poi.attributes.review.summary = 'I am invalid ACML'

      it 'clears errors after they have been fixed', ->
        @poi.validateContent()
        @poi.attributes.review.summary = '<p>I am valid ACML</p>'
        @poi.validateContent()
        expect(@poi.errors.length).toBe(0)

    describe 'with invalid ACML in review summary', ->

      beforeEach ->
        @review_summary = 'I am invalid summary ACML'
        @poi.attributes.review.summary = @review_summary
        spyOn($, 'acmlSummary').andCallFake -> "Summarized poi summary"

      it 'is invalid', ->
        expect(@poi.validateContent()).toBeFalsy()

      it 'summarizes the acml', ->
        @poi.validateContent()
        expect($.acmlSummary).toHaveBeenCalledWith(@review_summary)

      it 'stores validation errors', ->
        @poi.validateContent()
        expect(@poi.errors).toEqual ["Validation error in text starting with 'Summarized poi summary'"]

    describe 'with invalid ACML in review detail', ->

      beforeEach ->
        @review_detail = 'I am invalid detail ACML'
        @poi.attributes.review.detail = @review_detail
        spyOn($, 'acmlSummary').andCallFake -> 'Summarized poi detail'

      it 'is invalid', ->
        expect(@poi.validateContent()).toBeFalsy()

      it 'summarizes the acml', ->
        @poi.validateContent()
        expect($.acmlSummary).toHaveBeenCalledWith(@review_detail)

      it 'stores validation errors', ->
        @poi.validateContent()
        expect(@poi.errors).toEqual ["Validation error in text starting with 'Summarized poi detail'"]

    describe 'with valid ACML in all fields', ->

      beforeEach ->
        @poi.attributes.review.summary = '<p>I am valid summary ACML</p>'
        @poi.attributes.review.detail = '<p>I am valid detail ACML</p>'

      it 'is valid', ->
        expect(@poi.validateContent()).toBeTruthy()

      it 'has no save errors', ->
        @poi.validateContent()
        expect(@poi.state.get('saveErrors')).toBeFalsy()

  describe 'reporting errors', ->
    beforeEach ->
      spyOn(DSC, 'trigger')

    describe 'when there are errors', ->

      beforeEach ->
        @poi.errors = ['Oopsie doodle', 'Mrs Hoover...']

      it 'reports errors individually and includes the poi name', ->
        @poi.reportErrors()

        expect(DSC.trigger).toHaveBeenCalledWith(DSC.events.CONTENT_SAVE_ERROR, "Poi: Jonathan Apple - Oopsie doodle")
        expect(DSC.trigger).toHaveBeenCalledWith(DSC.events.CONTENT_SAVE_ERROR, "Poi: Jonathan Apple - Mrs Hoover...")

      it 'has save errors', ->
        @poi.reportErrors()
        expect(@poi.state.get('hasSaveErrors')).toBeTruthy()

    describe 'when there are no errors', ->

      beforeEach ->
        @poi.errors = []

      it 'reports nothing', ->
        @poi.reportErrors()
        expect(DSC.trigger).not.toHaveBeenCalled()

      it 'does not have save errors', ->
        @poi.reportErrors()
        expect(@poi.state.get('hasSaveErrors')).toBeFalsy()

  describe 'when there is a change', ->

    beforeEach ->
      @validateStub = spyOn(@poi, 'validateContent')
      @wordCountStub = spyOn(@poi, 'calculateWordCount')
      callDebounceFunctionsImmediately()
      @poi.set(foo: 'bar')

    it 'validates', ->
      expect(@poi.validateContent).toHaveBeenCalled()

    it 'calculates word count', ->
      expect(@poi.calculateWordCount).toHaveBeenCalled()

  describe '#friendlyName', ->

    it 'contains the type, name and id', ->
      expect(@poi.friendlyName()).toEqual("POI #{@poi.get('name')} (#{@poi.id})")

