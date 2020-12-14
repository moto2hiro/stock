import * as AppConsts from '../../AppConsts';

import {
  Button,
  ButtonGroup,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  Divider,
  Grid,
  IconButton,
  MenuItem,
  Popover,
  Snackbar,
  TextField,
} from '@material-ui/core';

import { Chart } from 'react-google-charts';
import CloseIcon from '@material-ui/icons/Close';
import FormUtils from '../../appUtils/FormUtils';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';
import React from 'react';
import TimelineIcon from '@material-ui/icons/Timeline';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  textField: {
    marginBottom: theme.spacing(3),
    width: 200,
    '& .MuiSelect-icon': {
      position: 'relative',
    },
  },
  extendedIcon: {
    marginRight: theme.spacing(1),
  },
  popover: {
    padding: theme.spacing(2),
    maxWidth: 200,
    wordWrap: 'break-word',
  },
}));

export default function ChartSandboxTemplate(state) {
  const classes = useStyles();
  const [popoverAnchorEl, setPopoverAnchorEl] = React.useState(null);
  const [isPopoverOpen, setPopoverOpen] = React.useState(false);
  const [popoverContent, setPopoverContent] = React.useState(false);
  const onOpenPopover = (content) => (event) => {
    setPopoverAnchorEl(event.currentTarget);
    setPopoverOpen((prev) => !prev);
    setPopoverContent(content);
  };
  const onClosePopover = (event) => {
    setPopoverAnchorEl(null);
    setPopoverOpen((prev) => !prev);
    setPopoverContent('');
  };

  return (
    <>
      <Grid container>
        <Grid item xs={12}>
          <Card>
            <CardHeader title='Set Up'></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container spacing={2} display='flex' alignItems='flex-end' alignContent='flex-end'>
                <Grid item xs={12} className='mb-0 pb-0'>
                  <h4 className='mb-0 pb-0 font-weight-normal'>Chart</h4>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    select
                    name='is_random_symbols'
                    label='Random Symbols'
                    value={state.request.is_random_symbols}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    className={classes.textField}
                    error={state.validation.formData.is_random_symbols?.isInvalid}
                    helperText={state.validation.formData.is_random_symbols?.message}
                  >
                    <MenuItem value={true}>True</MenuItem>
                    <MenuItem value={false}>False</MenuItem>
                  </TextField>
                </Grid>
                {state.request.is_random_symbols ? (
                  <>
                    <Grid item lg={3} md={6} sm={12} xs={12}>
                      <TextField
                        name='no_of_charts'
                        label='Number of Charts'
                        value={state.request.no_of_charts}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 1 }}
                        className={classes.textField}
                        error={state.validation.formData.no_of_charts?.isInvalid}
                        helperText={state.validation.formData.no_of_charts?.message}
                      />
                    </Grid>
                  </>
                ) : (
                  <>
                    <Grid item lg={3} md={6} sm={12} xs={12}>
                      <TextField
                        name='symbol'
                        label='Symbol'
                        value={state.request.symbol}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        className={classes.textField}
                        error={state.validation.formData.symbol?.isInvalid}
                        helperText={state.validation.formData.symbol?.message}
                      />
                    </Grid>
                  </>
                )}
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='date_from'
                    label='Date From'
                    value={state.request.date_from}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='date'
                    className={classes.textField}
                    error={state.validation.formData.date_from?.isInvalid}
                    helperText={state.validation.formData.date_from?.message}
                  />
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='date_to'
                    label='Date To'
                    value={state.request.date_to}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='date'
                    className={classes.textField}
                    error={state.validation.formData.date_to?.isInvalid}
                    helperText={state.validation.formData.date_to?.message}
                  />
                </Grid>
                <Grid item xs={12} className='mb-0 pb-0'>
                  <h4 className='mb-0 pb-0 font-weight-normal'>
                    Simple Moving Average Line
                    <IconButton
                      color='secondary'
                      onClick={onOpenPopover('Simple Moving Average trend lines.')}
                      className='p-0'
                    >
                      <HelpOutlineIcon />
                    </IconButton>
                  </h4>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    select
                    name='is_exclude_sma'
                    label='Exclude'
                    value={state.request.is_exclude_sma}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    className={classes.textField}
                    error={state.validation.formData.is_exclude_sma?.isInvalid}
                    helperText={state.validation.formData.is_exclude_sma?.message}
                  >
                    <MenuItem value={true}>True</MenuItem>
                    <MenuItem value={false}>False</MenuItem>
                  </TextField>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='sma_period_1'
                    label='SMA Period 1'
                    value={state.request.sma_period_1}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 1 }}
                    className={classes.textField}
                    error={state.validation.formData.sma_period_1?.isInvalid}
                    helperText={state.validation.formData.sma_period_1?.message}
                  />
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='sma_period_2'
                    label='SMA Period 2'
                    value={state.request.sma_period_2}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 1 }}
                    className={classes.textField}
                    error={state.validation.formData.sma_period_2?.isInvalid}
                    helperText={state.validation.formData.sma_period_2?.message}
                  />
                </Grid>
                <Grid item xs={12} className='mb-0 pb-0'>
                  <h4 className='mb-0 pb-0 font-weight-normal'>
                    Exponential Smoothing Line
                    <IconButton
                      color='secondary'
                      onClick={onOpenPopover('Smoothed prices using EMA to reduce noise.')}
                      className='p-0'
                    >
                      <HelpOutlineIcon />
                    </IconButton>
                  </h4>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    select
                    name='is_exclude_exponential_smoothing_prices'
                    label='Exclude'
                    value={state.request.is_exclude_exponential_smoothing_prices}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    className={classes.textField}
                    error={state.validation.formData.is_exclude_exponential_smoothing_prices?.isInvalid}
                    helperText={state.validation.formData.is_exclude_exponential_smoothing_prices?.message}
                  >
                    <MenuItem value={true}>True</MenuItem>
                    <MenuItem value={false}>False</MenuItem>
                  </TextField>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='exponential_smoothing_prices_shift'
                    label='Shift'
                    value={state.request.exponential_smoothing_prices_shift}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 0.01 }}
                    className={classes.textField}
                    error={state.validation.formData.exponential_smoothing_prices_shift?.isInvalid}
                    helperText={state.validation.formData.exponential_smoothing_prices_shift?.message}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton
                            color='secondary'
                            onClick={onOpenPopover('Multiplier to move the line.')}
                            className='p-0'
                          >
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='exponential_smoothing_alpha'
                    label='Alpha'
                    value={state.request.exponential_smoothing_alpha}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    error={state.validation.formData.exponential_smoothing_alpha?.isInvalid}
                    helperText={state.validation.formData.exponential_smoothing_alpha?.message}
                    type='number'
                    inputProps={{ step: 0.01 }}
                    className={classes.textField}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton
                            color='secondary'
                            onClick={onOpenPopover(
                              'A value between 0 and 1 to control smoothing. 0 with the least noise and vice versa.'
                            )}
                            className='p-0'
                          >
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
                <Grid item xs={12} className='mb-0 pb-0'>
                  <h4 className='mb-0 pb-0 font-weight-normal'>
                    Exponential Smoothing Max/Min
                    <IconButton
                      color='secondary'
                      onClick={onOpenPopover('Local Max/Min of the Exponentially Smoothed prices.')}
                      className='p-0'
                    >
                      <HelpOutlineIcon />
                    </IconButton>
                  </h4>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    select
                    name='is_exclude_exponential_smoothing_max_min'
                    label='Exclude'
                    value={state.request.is_exclude_exponential_smoothing_max_min}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    className={classes.textField}
                    error={state.validation.formData.is_exclude_exponential_smoothing_max_min?.isInvalid}
                    helperText={state.validation.formData.is_exclude_exponential_smoothing_max_min?.message}
                  >
                    <MenuItem value={true}>True</MenuItem>
                    <MenuItem value={false}>False</MenuItem>
                  </TextField>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='exponential_smoothing_max_min_diff'
                    label='Max/Min Diff'
                    value={state.request.exponential_smoothing_max_min_diff}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 0.01 }}
                    className={classes.textField}
                    error={state.validation.formData.exponential_smoothing_max_min_diff?.isInvalid}
                    helperText={state.validation.formData.exponential_smoothing_max_min_diff?.message}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton
                            color='secondary'
                            onClick={onOpenPopover('Threshold to control number of local max/mins.')}
                            className='p-0'
                          >
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
                <Grid item xs={12} className='mb-0 pb-0'>
                  <h4 className='mb-0 pb-0 font-weight-normal'>
                    Adaptive Bands Z Test-Statistics
                    <IconButton
                      color='secondary'
                      onClick={onOpenPopover("Bollinger Bands that adapt using Kaufman's Efficiency Ratio.")}
                      className='p-0'
                    >
                      <HelpOutlineIcon />
                    </IconButton>
                  </h4>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    select
                    name='is_exclude_abz'
                    label='Exclude'
                    value={state.request.is_exclude_abz}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    className={classes.textField}
                    error={state.validation.formData.is_exclude_abz?.isInvalid}
                    helperText={state.validation.formData.is_exclude_abz?.message}
                  >
                    <MenuItem value={true}>True</MenuItem>
                    <MenuItem value={false}>False</MenuItem>
                  </TextField>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='abz_er_period'
                    label='Efficiency Ratio Period'
                    value={state.request.abz_er_period}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 1 }}
                    className={classes.textField}
                    error={state.validation.formData.abz_er_period?.isInvalid}
                    helperText={state.validation.formData.abz_er_period?.message}
                  />
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='abz_std_distance'
                    label='Standard Deviation Distance'
                    value={state.request.abz_std_distance}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 0.01 }}
                    className={classes.textField}
                    error={state.validation.formData.abz_std_distance?.isInvalid}
                    helperText={state.validation.formData.abz_std_distance?.message}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton
                            color='secondary'
                            onClick={onOpenPopover(
                              'Upper/Lower Distance away from the middle band measured in standard deviations.'
                            )}
                            className='p-0'
                          >
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='abz_constant_k'
                    label='Constant K'
                    value={state.request.abz_constant_k}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 0.01 }}
                    className={classes.textField}
                    error={state.validation.formData.abz_constant_k?.isInvalid}
                    helperText={state.validation.formData.abz_constant_k?.message}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton color='secondary' onClick={onOpenPopover('Some contant K.')} className='p-0'>
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
              </Grid>
            </CardContent>
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <ButtonGroup fullWidth>
                    <Button
                      size='large'
                      variant='contained'
                      color='secondary'
                      onClick={state.onClickGetCharts}
                      disabled={state.is_processing}
                    >
                      <TimelineIcon className={classes.extendedIcon} />
                      Get Charts
                    </Button>
                  </ButtonGroup>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
          {state.has_run_get_charts === true && (
            <Grid item xs={12} className='mt-5'>
              <Card>
                <CardHeader title='Results' className='resultsDiv'></CardHeader>
                <Divider light={true} />
                <CardContent>
                  {state.is_processing ? (
                    <Grid container justify='center'>
                      <Grid item xs={1}>
                        <CircularProgress />
                      </Grid>
                    </Grid>
                  ) : !state.chartItems?.length ? (
                    <Grid container justify='center'>
                      <Grid item xs={12} align='center'>
                        No results found.
                      </Grid>
                    </Grid>
                  ) : (
                    <Grid container>
                      {state.chartItems.map((item, idx) => {
                        return (
                          <Grid item xs={12} key={idx} className='mb-3'>
                            <Chart
                              chartType={AppConsts.GOOGLE_CHART_TYPE_COMBO}
                              data={item}
                              width='100%'
                              height='700px'
                              options={state.chartOptions}
                            ></Chart>
                          </Grid>
                        );
                      })}
                    </Grid>
                  )}
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </Grid>
      <Popover
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={isPopoverOpen}
        anchorEl={popoverAnchorEl}
        onClose={onClosePopover}
      >
        {<div className={classes.popover}>{popoverContent}</div>}
      </Popover>
      <Snackbar
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        open={state.is_snackbar_open}
        autoHideDuration={6000}
        onClose={state.onCloseSnackbar}
        message={<span>{state.snackbar_content}</span>}
        action={[
          <IconButton key='close' aria-label='Close' color='inherit' className='p-1' onClick={state.onCloseSnackbar}>
            <CloseIcon />
          </IconButton>,
        ]}
      />
    </>
  );
}
